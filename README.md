# Remote Cash Register Closer
Allow people to close a cash register remotely using Slack

## Deployment  :rocket:
To deploy this into a Raspberry Pi (model 3B) you need to follow this steps

### Get yourself some tokens and URLs :globe_with_meridians:
- You will need an Slack API token and URL for the target app

- You will need a (free) [Ngrok token](https://ngrok.com/)


### On your Raspberry Pi :computer:
- Make sure your Raspberry time is in the proper timezone
- Enable IC2 on the Raspberry Pi
    - Follow [this guide](http://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/) (Sections ENABLE I2C IN RASPI-CONFIG and INSTALL I2C-TOOLS AND SMBUS) 

- Make sure you can run `python3` and `pip3`

- [Grab one of our releases](https://github.com/facevedom/remote-cash-register-controller/) `(dist.tar.gz)`

- Unzip our installer
``` bash
$ mkdir temp && tar xvfz dist.tar.gz temp
```

- Modify [config.ini](config.ini). You only need to change:
    - `WORKING_DIRECTORY` (if you want to customize the installation path)
    - `IC_ADDRESS` with the IC2 address of your Raspberry Pi
    - And add cash registers in the expected format

- Run the installer, replacing the tokens and URLs
```
$ sudo ./install *Ngrok-token* *slack-url* *slack-token*
```
That's it!. This will set up Ngrok as needed, display the Ngrok URLs on a LCD screen (connected on `SDA1` and `SCL1` pins), and **it will start the application**.

- Grab the Ngrok application URL (mapped to `localhost:5000`) and add it to your Slack app

## Stopping / Starting / Restarting / Checking status :no_mouth:
> Logs are stored in the installation path, under `application.log`

#### Ngrok
```
$ sudo service ngrok start
```
```
$ sudo service ngrok stop
```
```
$ sudo service ngrok restart
```
```
$ sudo service ngrok status
```
> Everytime you restart the Ngrok service (or the Raspberry restarts), you'll need to update your new public URL in the Slack web app management console!

#### This application
```
$ sudo service cash_register_closer start
```
```
$ sudo service cash_register_closer stop
```
```
$ sudo service cash_register_closer restart
```
```
$ sudo service cash_register_closer status
```
> Everytime this application is started, it will check if Ngrok is running. If it is not running, Ngrok service will be started. If it is already running, this application will leave it alone :smile:

## Running the tests :scream:
> This will only run on a Raspberry Pi 3B
```
$ python3 test.py
```

## Caveats & Considerations :sweat_smile:
- No other software can use Ngrok on the Raspberry when this is installed
- This will install it's Python dependencies globally for your root user

## Built With :hammer:
- [Flask](http://flask.pocoo.org/) - The web framework used
- [Raspberry Pi](https://www.raspberrypi.org/) - The platform
- [SQLite](https://www.sqlite.org/index.html) - The database library

## Authors :construction_worker: :construction_worker:
- **Felipe Acevedo** - [facevedom](https://github.com/PurpleBooth)
- **Juan Mejia** - [JuanGMejia](https://github.com/JuanGMejia)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
