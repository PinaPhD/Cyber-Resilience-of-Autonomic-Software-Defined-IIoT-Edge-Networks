---
### To upgrade from XFCE4 to GNOME on the Ubuntu System


1. Update the system

```bash
   sudo apt update && sudo apt upgrade -y 
   sudo apt install ubuntu-gnome-desktop -y
   sudo dpkg-reconfigure gdm3
   sudo apt purge xfce4 xfce4-* && sudo apt autoremove --purge -y
   sudo reboot
   
```



