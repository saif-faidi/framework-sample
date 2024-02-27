
def tcp_send(*data):
    value = data[0]
    print(value)

def mqtt_send(*data):
    data, topic, qos, retain = data
    print(data)

if __name__ == "__main__":
    tcp_send('value', 'Topic', 2, False)
    tcp_send("value", "other parameters")