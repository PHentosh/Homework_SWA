# Homework_SWA

У цій домашці реалізовано збереження логів на Hazelcast нодах чрез logging-service.

Hazelcast ноди та logging-service ноди запускаються окремо, але для кожної lodding ноди є своя відповідна hazelcast нода.

Facade-service рандомно вибирає одну з доступних нод, щоб надсилати логи.

Увесь проект запескається черех docker-compose

Щоб запустити проект:
```
$> docker-compose build
$> docker-compose up -d
```

Щоб вимкнути все:
```
$> docker-compose down
```

## Надсилання запитів

Ось приклади успішного надсиання POST та GET запитів на facede-service

![post](facade/post.png)

![get](facade/get.png)

Оскільки ноди для логування вибираються випадковим чином, то кожна буде мати свої меседжі, але при витягування всіх повідомлень, кожна нода може вернути всі повідомлення, що були залоговані.

![log1](logging-1/logging_1.png)

![log2](logging-2/logging_2.png)

![log3](logging-3/logging_3.png)

Також, завдяки hazelcast навіть при вимкнені одної чи двох нод логування і hazelcast всі повідомлення лишаються збереженими

![one_out](facade/one_node_down.png)
![one_out](facade/two_node_down.png)
