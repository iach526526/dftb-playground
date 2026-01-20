#/bin/sh
cow() {
	  MSG="$1"
cat <<EOF
	     ______
	     < $MSG >
	      ------
	              \   ^__^
		       \  (oo)\_______
			  (__)\       )\/\ 
			   ||------w||
			   ||       ||
										   
EOF
 }

cow "Hi! I am dftb+ quick setup wizard made by Each"
cd parameters/
chmod +x ./setup-param.sh
./setup-param.sh
