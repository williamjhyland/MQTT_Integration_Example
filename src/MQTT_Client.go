package main

import (
	"encoding/json"
	"log"
	"os"
	"time"

	mqtt "github.com/eclipse/paho.mqtt.golang"
)

var logger = log.New(os.Stdout, "", log.LstdFlags)

type MQTTClient struct {
	client mqtt.Client
	topic  string
	host   string
	port   int
	qos    byte
}

func NewMQTTClient(topic, host string, port int, qos byte) *MQTTClient {
	opts := mqtt.NewClientOptions()
	opts.AddBroker("tcp://" + host + ":" + string(port))
	opts.SetClientID("go_mqtt_client")
	opts.SetDefaultPublishHandler(messageHandler)

	client := mqtt.NewClient(opts)
	if token := client.Connect(); token.Wait() && token.Error() != nil {
		logger.Fatalf("Error connecting to MQTT broker: %s", token.Error())
	}

	return &MQTTClient{
		client: client,
		topic:  topic,
		host:   host,
		port:   port,
		qos:    qos,
	}
}

func (m *MQTTClient) Subscribe() {
	if token := m.client.Subscribe(m.topic, m.qos, nil); token.Wait() && token.Error() != nil {
		logger.Fatalf("Error subscribing to topic %s: %s", m.topic, token.Error())
	}
	logger.Printf("Subscribed to topic %s", m.topic)
}

func (m *MQTTClient) Publish(payload interface{}) {
	msg, err := json.Marshal(payload)
	if err != nil {
		logger.Printf("Error marshaling payload: %s", err)
		return
	}

	token := m.client.Publish(m.topic, m.qos, false, msg)
	token.Wait()
}

func (m *MQTTClient) Disconnect() {
	m.client.Disconnect(250)
}

func messageHandler(client mqtt.Client, msg mqtt.Message) {
	logger.Printf("Received message: %s from topic: %s\n", msg.Payload(), msg.Topic())
}

func main() {
	topic := "your/topic"
	host := "localhost"
	port := 1883
	qos := byte(1)

	mqttClient := NewMQTTClient(topic, host, port, qos)
	mqttClient.Subscribe()

	// Example payload
	payload := map[string]string{"key": "value"}
	mqttClient.Publish(payload)

	// Run for some time and then disconnect
	time.Sleep(60 * time.Second)
	mqttClient.Disconnect()
}
