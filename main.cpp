#include <iostream>
#include <opencv2/core/core.hpp>

// Drawing shapes
#include <opencv2/imgproc.hpp>

#include <opencv2/highgui/highgui.hpp>
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


            flip(frame, frame, 1);      //this flip the img so it is more intuitive for the user
            //we flip first so we don't have to flip the other data, like the squares shown



            Point start_point(5, 5);

            //Ending coordinate, here (220, 220)
            //represents the bottom right corner of rectangle
            Point end_point(220, 220);

            //Blue color in BGR

            //Line thickness of 2 px
            int thickness = 2;

            //Using cv2.rectangle() method
            //Draw a rectangle with blue line borders of thickness of 2 px
            rectangle(frame, start_point, end_point,
                          Scalar(0, 255, 255),
                          thickness, 8, 0);





            imshow("testframe", frame);
            pressedKey=waitKey(1);
        }
        destroyWindow("testvid");
        capture.release();
    }


    //end program
    return 0;
}
