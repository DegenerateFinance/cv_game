#include <opencv2/highgui.hpp>  //esto se supone q incluye las librerías
#include <iostream>
// makefile con esto  g++ test.cpp -o testoutput -std=c++11 `pkg-config --cflags --libs opencv`

using namespace std;
using namespace cv;
#define ESCAPE  27

int main( int argc, char** argv )
{

    Mat frame;

    VideoCapture capture(0);

    char pressedKey =0;

    bool success;


    if(!capture.isOpened() )
    {
        cout<<"Error loading video"<<endl;
    }
    else
    {
        namedWindow("testvid", WINDOW_AUTOSIZE);

        while(pressedKey != ESCAPE )
        {
            success=capture.read(frame);

            if (success==false)
            {
                cout<<"Can't read frame from file"<<endl;
                return 1;
            }

            imshow("testframe", frame);

            pressedKey=waitKey(1);
        }
        destroyWindow("testvid");
        capture.release();
    }


    //end program
    return 0;
}
