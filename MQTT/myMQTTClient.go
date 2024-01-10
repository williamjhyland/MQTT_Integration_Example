package myMQTTClient

import (
	"context"
	"errors"
	"fmt"
	"log"
	"sync"

	mqtt "github.com/eclipse/paho.mqtt.golang"
	"go.viam.com/rdk/components/sensor"
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/resource"
)

// Init called upon import, registers this component with the module
func init() {
	resource.RegisterComponent(sensor.API, Model, resource.Registration[sensor.Sensor, *Config]{Constructor: newSensor})
}

// To be used for functions which are not meant to be implemented in your component
var errUnimplemented = errors.New("unimplemented")

// Your model's colon-delimited-triplet (acme:demo:mybase). acme = namespace, demo = repo-name, mybase = model name
// If you plan to upload this module to the Viam registry, "acme" must match your Viam registry namespace.
var Model = resource.NewModel("bill", "mqtt", "json")

// Maps JSON component configuration attributes.
type Config struct {
	topic string `json:"topic"`
	host  string `json:"host"`
	port  int    `json:"port"`
	qos   int    `json:"qos"`
}

// Implement component configuration validation and and return implicit dependencies.
func (cfg *Config) Validate(path string) ([]string, error) {
	// Check if the topic is set
	if cfg.topic == "" {
		return nil, fmt.Errorf("topic is required for MQTT_Client %q", path)
	}

	// Check if the host is set
	if cfg.host == "" {
		return nil, fmt.Errorf("host is required for MQTT_Client %q", path)
	}

	// Check if the port is valid
	if cfg.port <= 0 {
		return nil, fmt.Errorf("invalid port (should be > 0) for MQTT_Client %q", path)
	}

	// Check if qos is within a valid range (usually 0 to 2 for MQTT)
	if cfg.qos < 0 || cfg.qos > 2 {
		return nil, fmt.Errorf("qos must be between 0 and 2 for MQTT_Client %q", path)
	}

	return []string{}, nil
}

type MQTT_Client struct {
	resource.Named
	logger        logging.Logger
	client        mqtt.Client
	topic         string
	host          string
	port          int
	qos           byte
	latestMessage string
	mutex         sync.Mutex
}

// Sensor type constructor.
// Called upon sensor instantiation when a sensor model is added to the machine configuration
func newSensor(ctx context.Context, deps resource.Dependencies, conf resource.Config, logger logging.Logger) (sensor.Sensor, error) {
	s := &MQTT_Client{
		Named:  conf.ResourceName().AsNamed(),
		logger: logger,
	}
	if err := s.Reconfigure(ctx, deps, conf); err != nil {
		return nil, err
	}
	return s, nil
}

// Reconfigure reconfigures with new settings.
func (s *MQTT_Client) Reconfigure(ctx context.Context, deps resource.Dependencies, conf resource.Config) error {
	// Convert the generic resource.Config to the MQTT_Client-specific Config structure
	clientConfig, err := resource.NativeConfig[*Config](conf)
	if err != nil {
		return err
	}

	// Reconfigure the MQTT_Client instance with new settings from clientConfig
	s.topic = clientConfig.topic
	s.host = clientConfig.host
	s.port = clientConfig.port
	s.qos = byte(clientConfig.qos) // Assuming qos in Config is an int and needs conversion to byte

	// Log the new configuration (optional, adjust logging as needed)
	s.logger.Infof("Reconfigured MQTT_Client with topic: %s, host: %s, port: %d, qos: %d", s.topic, s.host, s.port, s.qos)

	return err
}

// Get sensor reading
func (s *MQTT_Client) Readings(ctx context.Context, _ map[string]interface{}) (map[string]interface{}, error) {
	s.mutex.Lock()
	defer s.mutex.Unlock()

	return map[string]interface{}{
		"latestMessage": s.latestMessage,
	}, nil
}

// DoCommand can be implemented to extend sensor functionality but returns unimplemented in this example.
func (s *MQTT_Client) DoCommand(ctx context.Context, cmd map[string]interface{}) (map[string]interface{}, error) {
	return nil, errUnimplemented
}

// New function to initialize MQTT client and start the goroutine
func (s *MQTT_Client) InitMQTTClient(ctx context.Context, config MQTT_Client) error {
	// Create a client and connect to the broker
	opts := mqtt.NewClientOptions()
	opts.AddBroker(fmt.Sprintf("tcp://%s:%d", config.host, config.port))
	opts.SetClientID("your_client_id") // Set a unique client ID

	s.client = mqtt.NewClient(opts)
	if token := s.client.Connect(); token.Wait() && token.Error() != nil {
		return token.Error()
	}

	// Start the goroutine to listen to the topic
	go func() {
		if token := s.client.Subscribe(config.topic, config.qos, func(client mqtt.Client, msg mqtt.Message) {
			s.mutex.Lock()
			s.latestMessage = string(msg.Payload())
			s.mutex.Unlock()
		}); token.Wait() && token.Error() != nil {
			// Handle subscription error
			log.Println("Subscription error:", token.Error())
		}
	}()

	return nil
}

// Add a Close method to clean up the MQTT client
func (s *MQTT_Client) Close(ctx context.Context) error {
	if s.client != nil && s.client.IsConnected() {
		s.client.Disconnect(250) // Timeout in milliseconds
	}
	return nil
}
