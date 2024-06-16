# Лабораторная работа №1

Проект лабораторной работы представлен в файле `lab1.unl`

### Схема сети

Схема сети представлена ниже

![image](https://github.com/egnees/networks_course/assets/84775607/fb93f0a4-20ea-48b5-8c3b-4485575074b9)


### Настройка компонентов

Ниже приведены команды, использованные для настройки компонентов

### VPC1
  ```
  VPCS> ip 10.0.10.1/24 10.0.10.100
  Checking for duplicate address...
  VPCS : 10.0.10.1 255.255.255.0 gateway 10.0.10.100
  ```
### VPC2
  ```
  VPCS> ip 10.0.20.1/24 10.0.20.100
  Checking for duplicate address...
  VPCS : 10.0.20.1 255.255.255.0 gateway 10.0.20.100
  ```
  
### Switch2
  ```
  Switch>enable
  Switch#configure terminal
  Switch(config)#vlan 10
  Switch(config-vlan)#exit
  Switch(config)#vlan 20
  Switch(config-vlan)#exit
  Switch(config)#interface Gi0/1
  Switch(config-if)#switchport mode access
  Switch(config-if)#switchport access vlan 10
  Switch(config-if)#exit
  Switch(config)#interface Gi0/0
  Switch(config-if)#switchport trunk encapsulation dot1q
  Switch(config-if)#switchport mode trunk
  Switch(config-if)#switchport trunk allowed vlan 10,20
  Switch(config-if)#exit
  Switch(config)#interface Gi0/2
  Switch(config-if)#switchport trunk encapsulation dot1q
  Switch(config-if)#switchport mode trunk
  Switch(config-if)#switchport trunk allowed vlan 10,20
  Switch(config-if)#exit
  Switch(config)#exit
  ```

### Switch3

Аналогично настраиваем `Switch3`, с той лишь разницей, что подключаем `VPS1` по порту `Gi0/1` к `vlan20.

### Switch1

Настраиваем все порты `Switch 1` аналогично порту `Gi0/0` устройства `Switch 2`, после чего выполняем следующее:

```
Switch(config)#spanning-tree mode pvst
Switch(config)#spanning-tree extend system-id
Switch(config)#spanning-tree vlan 10,20 priority 0
```

### Router

  ```
  Router>enable
  Router#configure terminal
  Router(config)#interface Gi0/0
  Router(config-if)#no shutdown
  Router(config-if)#exit
  Router(config)#exit
  Router(config)#interface Gi0/0.10
  Router(config-subif)#encapsulation dot1q 10
  Router(config-subif)#ip address 10.0.10.100 255.255.255.0
  Router(config-subif)#exit
  Router(config)#interface Gi0/0.20
  Router(config-subif)#encapsulation dot1q 20
  Router(config-subif)#ip address 10.0.20.100 255.255.255.0
  Router(config-subif)#exit
  Router(config)#exit
  ```

### Проверка

Проверим доступность `VPS2` из `VPS1`:
```
VPCS> ping 10.0.20.1

84 bytes from 10.0.20.1 icmp_seq=1 ttl=63 time=10.071 ms
84 bytes from 10.0.20.1 icmp_seq=2 ttl=63 time=6.101 ms
84 bytes from 10.0.20.1 icmp_seq=3 ttl=63 time=5.781 ms
84 bytes from 10.0.20.1 icmp_seq=4 ttl=63 time=5.754 ms
84 bytes from 10.0.20.1 icmp_seq=5 ttl=63 time=5.965 ms
```

Теперь `VPS1` из `VPS2`:
```
VPCS> pin 10.0.10.1

84 bytes from 10.0.10.1 icmp_seq=1 ttl=63 time=7.254 ms
84 bytes from 10.0.10.1 icmp_seq=2 ttl=63 time=6.181 ms
84 bytes from 10.0.10.1 icmp_seq=3 ttl=63 time=5.252 ms
84 bytes from 10.0.10.1 icmp_seq=4 ttl=63 time=6.109 ms
84 bytes from 10.0.10.1 icmp_seq=5 ttl=63 time=5.912 ms
```

### Остовное дерево сети

# Switch1
```
Switch>show spanning-tree

VLAN0010
Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/0               Desg FWD 4         128.1    P2p
Gi0/1               Desg FWD 4         128.2    P2p
Gi0/2               Desg FWD 4         128.3    P2p

VLAN0020
Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/0               Desg FWD 4         128.1    P2p
Gi0/1               Desg FWD 4         128.2    P2p
Gi0/2               Desg FWD 4         128.3    P2p
```

# Switch2
```
Switch>show spanning-tree

VLAN0010
Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/0               Root FWD 4         128.1    P2p
Gi0/1               Desg FWD 4         128.2    P2p
Gi0/2               Desg FWD 4         128.3    P2p

VLAN0020
Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/0               Root FWD 4         128.1    P2p
Gi0/2               Desg FWD 4         128.3    P2p
```
# Switch3
```
Switch>show spanning-tree

VLAN0010
Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/0               Root FWD 4         128.1    P2p
Gi0/2               Altn BLK 4         128.3    P2p

VLAN0020
Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/0               Root FWD 4         128.1    P2p
Gi0/1               Desg FWD 4         128.2    P2p
Gi0/2               Altn BLK 4         128.3    P2p
```

Как можно видеть, между `Switch2` и `Switch3` нет прямого соединения --- оно заблокировано, как и ожидалось.

### Fault tolerance

Далее проверим отказоустойчивость полученной сети, для этого выключим порт `Gi0/2` устройства `Switch2`.

```
Switch>enable
Switch#conf term
Enter configuration commands, one per line.  End with CNTL/Z.
Switch(config)#int Gi0/2
Switch(config-if)#shutdown
Switch(config-if)#exit
Switch(config)#exit
Switch#
```

Проверим доступность:
Из `VPS1` в `VPS2`:
```
VPCS> ping 10.0.20.1

84 bytes from 10.0.20.1 icmp_seq=1 ttl=63 time=10.05 ms
84 bytes from 10.0.20.1 icmp_seq=2 ttl=63 time=7.713 ms
84 bytes from 10.0.20.1 icmp_seq=3 ttl=63 time=6.127 ms
84 bytes from 10.0.20.1 icmp_seq=4 ttl=63 time=9.553 ms
84 bytes from 10.0.20.1 icmp_seq=5 ttl=63 time=6.411 ms
```

Из `VPS2` в `VPS1`:
```
VPCS> pin 10.0.10.1

84 bytes from 10.0.10.1 icmp_seq=1 ttl=63 time=8.544 ms
84 bytes from 10.0.10.1 icmp_seq=2 ttl=63 time=6.089 ms
84 bytes from 10.0.10.1 icmp_seq=3 ttl=63 time=7.064 ms
84 bytes from 10.0.10.1 icmp_seq=4 ttl=63 time=6.711 ms
84 bytes from 10.0.10.1 icmp_seq=5 ttl=63 time=6.53 ms
```



