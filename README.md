# live-container-migration
Implementation of MiGrror &amp; precopy utilizing CRIU and Podman.


## OS Compatibility
- **Ubuntu 22.04 LTS**

## Setup Instructions

To set up the necessary environment, follow these steps:

### 1. Install Required Python Libraries
Install the required Python libraries using pip:

```bash
pip install watchdog psutil

```
### 2. Install CRIU (Checkpoint/Restore In Userspace)
Install CRIU using the following command:

```bash
sudo apt-get install criu

```


### 3. Install Podman
To install Podman, use the command below:
```bash
sudo apt-get install podman
```



### 4. Grant Admin Access to CRIU
Ensure CRIU has the necessary permissions by running:
```bash
sudo setcap cap_sys_admin+ep $(which criu)
```
