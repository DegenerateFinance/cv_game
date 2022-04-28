all: main clone

main: main.cpp
	g++ main.cpp -o main_exe -std=c++11 `pkg-config --cflags --libs opencv`

clone_hand: hand.cpp
	g++ hand.cpp -o hand_exe -std=c++11 `pkg-config --cflags --libs opencv`

clean:
	rm -f main_exe hand_exe
