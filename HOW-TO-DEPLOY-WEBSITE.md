# Deployment websites #

There are a number of tools to transfer files from local to remote servers.

In case of LIACS you can log into https://ssh.liacs.nl server with your university name credentials.

This server is reachable by internet and acts like a proxy file server where the webserver is gettings its files from.

If you like command line tools you can choose PuTTY.

If you like windows tools you can choose WinSCP.

# Deployment with WinSCP for Windows #

Install WinSCP from 

```
https://winscp.net/eng/index.php
```

For login choose SFTP protocol port 22, and as host ssh.liacs.nl

Enter your university credentials in corresponding fields.

Say YES to the encryption key as to-be-trusted.

The webserver files can be found in /webhome/csuniversity/

![image](https://user-images.githubusercontent.com/37830964/210339057-197e13af-d0cc-48c4-a6bd-b1831ca669a1.png)

# Deployment with PuTTY for windows #

Use PuTTY to connect to the https://ssh.liacs.nl server.

This server is reachable via the WLAN3 network inside LIACS, sometimes outside LIACS (internet).

Or, set up a VPN LIACS connection with IKEv2 if outside LIACS, see VPN Access (IKEv2)_LIACS REL.pdf (see docs.liacs.nl inside LIACS).

PuTTY comes with a number of tools among them the PSFTP-tool. 

Download from:

```
https://www.chiark.greenend.org.uk/~sgtatham/putty
```

To transfer files to the server use PSFTP - Putty Secure File Transfer Protocol - to start from the appl search box in windows.

Start FSFTP

```
psftp: no hostname specified; use "open host.name" to connect
psftp> help
!      run a local command
bye    finish your SFTP session
cd     change your remote working directory
chmod  change file permissions and modes
close  finish your SFTP session but do not quit PSFTP
del    delete files on the remote server
dir    list remote files
exit   finish your SFTP session
get    download a file from the server to your local machine
help   give help
lcd    change local working directory
lpwd   print local working directory
ls     list remote files
mget   download multiple files at once
mkdir  create directories on the remote server
mput   upload multiple files at once
mv     move or rename file(s) on the remote server
open   connect to a host
put    upload a file from your local machine to the server
pwd    print your remote working directory
quit   finish your SFTP session
reget  continue downloading files
ren    move or rename file(s) on the remote server
reput  continue uploading files
rm     delete files on the remote server
rmdir  remove directories on the remote server
psftp> pwd
psftp: not connected to a host; use "open host.name"
psftp> mput
psftp: not connected to a host; use "open host.name"
psftp> put
psftp: not connected to a host; use "open host.name"
psftp> help put
put [ -r ] [ -- ] <filename> [ <remote-filename> ]
  Uploads a file to the server and stores it there under
  the same name, or under a different one if you supply the
  argument <remote-filename>.
  If -r specified, recursively store a directory.
psftp> help mput
mput [ -r ] [ -- ] <filename-or-wildcard> [ <filename-or-wildcard>... ]
  Uploads many files to the server, storing each one under the
  same name it has on the client side. You can use wildcards
  such as "*.c" to specify lots of files at once.
  If -r specified, recursively store files and directories.
psftp>open ssh.liacs.nl
```

Or use PSCP - Putty Secure CoPy - to start from the command prompt (set PATH=C:\Program Files\PuTTY or in the environment variables).

```
pscp c:/music.mp3  ubuntu@10.0.0.3:/home/ubuntu/Music

pscp ubuntu@10.0.0.3:/home/ubuntu/Music/music.mp3 c:/
```

See, https://community.nxp.com/t5/i-MX-Processors/Copying-Files-Between-Windows-and-Linux-using-PuTTY/m-p/145880

## Login with your UL-name credentials ##

To login use your university name and password.

There is a webhome directory placed under the root directory where you can deploy your web related files.

In our case this is /webhome/csuniversity/

Set the local and remote directory to transfer files.

```
psftp: no hostname specified; use "open host.name" to connect
psftp> open ssh.liacs.nl
login as: uname
uname@ssh.liacs.nl's password: pw
Remote working directory is /home/uname
psftp> pwd
Remote directory is /home/uname
psftp> lpwd
Current local directory is C:\Program Files\PuTTY
psftp> lcd c:/liacsprojects/lucd/front-end/liacsserver
New local directory is c:\liacsprojects\lucd\front-end\liacsserver
psftp> cd /webhome/csunivercity
Remote directory is now /webhome/csunivercity
psftp> pwd
Remote directory is /webhome/csunivercity
psftp> ls
Listing directory /webhome/csunivercity
drwxrws---    1 510035   cswwwdata        3 Aug  3 16:58 .
drwxr-xr-x    1 root     cswwwdata      635 Sep  2 12:09 ..
drwxrws---    1 rietveldkfd cswwwdata        2 Aug  4 07:14 application
drwxrws---    1 510035   cswwwdata        1 Sep  5 16:47 public_html
drwxrws---    1 rietveldkfd cswwwdata        8 Aug  3 16:51 pyenv
psftp> cd application
Remote directory is now /webhome/csunivercity/application
psftp> ls
Listing directory /webhome/csunivercity/application
drwxrws---    1 rietveldkfd cswwwdata        2 Aug  4 07:14 .
drwxrws---    1 510035   cswwwdata        3 Aug  3 16:58 ..
-rw-rw----    1 rietveldkfd cswwwdata      213 Aug  4 07:12 myapp.wsgi
-rw-rw----    1 rietveldkfd cswwwdata      809 Aug  4 07:07 test.py
```

Use the following commands to transfer the files from local to remote server:

```
psftp> mput -r dashboard *    Put file on the server
psftp> mget * *               Get files from the server
psftp> lpwd                   Path of local host
psftp> pwd                    Path of server
psftp> lcd                    Change directory local host
psftp> cd                     Change directory server
```

Here follows an example for linking_UCD to update a new landing page index.html:

Start PSFTP.exe  

```
psftp: no hostname specified; use "open host.name" to connect
psftp> open ssh.liacs.nl
login as: uname
uname@ssh.liacs.nl's password:
Remote working directory is /home/uname
psftp> cd /webhome/csunivercity/public_html
Remote directory is now /webhome/csunivercity/public_html
psftp> ls
Listing directory /webhome/csunivercity/public_html
drwxrws---    1 510035   cswwwdata        1 Sep  7 13:49 .
drwxrws---    1 510035   cswwwdata        4 Sep  7 13:41 ..
-rw-rw----    1 kraaijw  cswwwdata     2537 Sep  7 19:39 index.html
psftp> lcd C:\LiacsProjects\LUCD\Front-end\LIACSserver\public_html
New local directory is C:\LiacsProjects\LUCD\Front-end\LIACSserver\public_html
psftp> lpwd
Current local directory is C:\LiacsProjects\LUCD\Front-end\LIACSserver\public_html
psftp> mput index.html
local:index.html => remote:/webhome/csunivercity/public_html/index.html
psftp>
```
