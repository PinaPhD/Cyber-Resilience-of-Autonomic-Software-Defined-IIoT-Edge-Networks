---
### To upgrade from XFCE4 to GNOME on the Ubuntu System

![Ubuntu GNOME](https://diocesanos.es/blogs/equipotic/wp-content/uploads/sites/2/2017/09/ubuntu-gnome-logo.png)

1. Update the system

```bash
   sudo apt update && sudo apt upgrade -y 
```

2. Install GNOME full version

```bash
   sudo apt install ubuntu-gnome-desktop -y
```

3. Configure the display manager

```bash
   sudo dpkg-reconfigure gdm3
```

4. Reboot the system

```bash
   sudo reboot
```

5. Remove the XFCE4 version

```bash
   sudo apt purge xfce4 xfce4-* && sudo apt autoremove --purge -y
```


