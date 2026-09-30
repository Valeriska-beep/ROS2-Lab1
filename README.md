# Лабораторна робота №1
## Архітектура ROS2. Реалізація Publisher / Subscriber

## 1. Перевірка встановлення ROS2 та запуск turtlesim

### 1.1. Перевірка встановлення ROS2

Виконати в терміналі:
```bash
ros2 doctor

```

### 1.2. Запуск turtlesim

В окремому терміналі:

```bash
ros2 run turtlesim turtlesim_node

```

### 1.3. Запуск teleop

В іншому терміналі:

```bash
ros2 run turtlesim turtle_teleop_key

```

### 1.4. Перевірка активних нод та топіків

```bash
ros2 node list
ros2 topic list

```

### 1.5. Перегляд повідомлень керування

```bash
ros2 topic echo /turtle1/cmd_vel

```

## 2. Створення власного пакету

### 2.1. Створення пакету

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python my_first_package --dependencies rclpy std_msgs

```

### 2.2. Збірка пакету

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash

```

### 2.3. Перевірка пакету

```bash
ros2 pkg list | grep my_first_package

```

## 3. Реалізація Publisher

### 3.1. Створення Publisher-ноди

```bash
cd ~/ros2_ws/src/my_first_package/my_first_package
nano publisher_node.py

```

### 3.2. Код publisher_node.py

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PublisherNode(Node):

    def __init__(self):
        super().__init__('publisher_node')

        self.publisher = self.create_publisher(
            String,
            'my_topic',
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_message
        )

    def publish_message(self):
        msg = String()
        msg.data = 'Hello ROS 2!'

        self.publisher.publish(msg)

        self.get_logger().info(
            f'Публікація: {msg.data}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = PublisherNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

```

### 3.3. Реєстрація Publisher у setup.py

```bash
cd ~/ros2_ws/src/my_first_package
nano setup.py

```

У `console_scripts` додати:

```python
'publisher_node = my_first_package.publisher_node:main',

```

### 3.4. Збірка та запуск Publisher

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
ros2 run my_first_package publisher_node

```

## 4. Реалізація Subscriber

### 4.1. Створення Subscriber-ноди

```bash
cd ~/ros2_ws/src/my_first_package/my_first_package
nano subscriber_node.py

```

### 4.2. Код subscriber_node.py

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SubscriberNode(Node):

    def __init__(self):
        super().__init__('subscriber_node')

        self.subscription = self.create_subscription(
            String,
            'my_topic',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        self.get_logger().info(
            f'Отримано: {msg.data}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = SubscriberNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

```

### 4.3. Реєстрація Subscriber у setup.py

```bash
nano ~/ros2_ws/src/my_first_package/setup.py

```

Блок `entry_points` має виглядати так:

```python
entry_points={
    'console_scripts': [
        'publisher_node = my_first_package.publisher_node:main',
        'subscriber_node = my_first_package.subscriber_node:main',
    ],
},

```

### 4.4. Збірка пакету

```bash
cd ~/ros2_ws
colcon build

```

### 4.5. Запуск Subscriber

```bash
source ~/ros2_ws/install/setup.bash
ros2 run my_first_package subscriber_node

```

## 5. Перевірка роботи системи

### 5.1. Запуск Publisher

**Термінал 1:**

```bash
source ~/ros2_ws/install/setup.bash
ros2 run my_first_package publisher_node

```

### 5.2. Запуск Subscriber

**Термінал 2:**

```bash
source ~/ros2_ws/install/setup.bash
ros2 run my_first_package subscriber_node

```

### 5.3. Перевірка нод та Topic

**Термінал 3:**

```bash
source ~/ros2_ws/install/setup.bash
ros2 node list
ros2 topic list
ros2 topic echo /my_topic

```

Publisher кожну секунду публікує повідомлення `Hello ROS 2!` у Topic `/my_topic`.
Subscriber отримує ці повідомлення та виводить їх у консоль через ROS2 Logger.
