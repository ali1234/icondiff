
all:
	gcc -Wall -Werror -O0 -pipe \
	svgtopng.c -o svgtopng \
	`pkg-config --libs --cflags gtk+-2.0` \
        `pkg-config --libs --cflags libxfce4ui-1` \
        `pkg-config --libs --cflags gdk-pixbuf-2.0` \
        `pkg-config --libs --cflags gobject-2.0`
