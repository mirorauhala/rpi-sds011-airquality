# Raspberry Pi SDS011 Air Quality Monitor

Run with the following command:

```
git clone https://github.com/mirorauhala/rpi-sds011-airquality
```

```
cd rpi-sds011-airquality
```

```
docker build .
```

```
docker run -it --device=/dev/ttyUSB0 --restart=unless-stopped {{build_hash}}
```