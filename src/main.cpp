#include <ros/ros.h>
#include <std_msgs/Header.h>
#include <sensor_msgs/Image.h>
#include <opencv2/opencv.hpp>
#include <cv_bridge/cv_bridge.h>

#include <sstream>

#define WIDTH 640
#define HEIGHT 480
#define FREQUENCY 4
#define TOPIC "/camera/image_raw"

int main(int argc, char **argv)
{
    ros::init(argc, argv, "webcam");
    ros::NodeHandle node;
    ros::Publisher publisher = node.advertise<sensor_msgs::Image>(TOPIC, 2);

    cv::VideoCapture capture(0);
    if (!capture.isOpened())
	return 1;
    capture.set(3, WIDTH);
    capture.set(4, HEIGHT);

    cv::Mat grayscale;
    ros::Rate loop_rate(FREQUENCY);
    while (ros::ok())
    {
	cv::Mat frame;
	capture >> frame;
	cv::cvtColor(frame, grayscale, cv::COLOR_RGB2GRAY);
	cv_bridge::CvImage image(std_msgs::Header(), "mono8", grayscale);
	publisher.publish(image.toImageMsg());

	ros::spinOnce();
	loop_rate.sleep();
    }

    return 0;
}
