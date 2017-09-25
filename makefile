install:
	cp sshh.sh /usr/bin/sshh
	chmod +x /usr/bin/sshh

	cp -r sshh.src/ /usr/bin/sshh.src/
	cp sshh.src/_sshh_completion.sh /etc/profile.d/_sshh_completion.sh
