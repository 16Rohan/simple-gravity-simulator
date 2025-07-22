#include <iostream>
#include <glad/glad.h>
#include <GLFW/glfw3.h>
using namespace std;

int main()
{
    //initalise GLFW
    glfwInit();

    // Tell GLFW what version of opengl we are using which is 3.3
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);

    //tell glfw we are using core profile 
    // so that means we only have the modern features 
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow *window = glfwCreateWindow(800, 800, "Test", NULL, NULL); // height, width, name, you want full screen, not important

    //error checking 
    if (window == NULL)
    {
        cout << "Failed to create GLFW window" << endl;
        glfwTerminate();
        return -1;
    }


    glfwMakeContextCurrent(window); // make the window for the current context

    gladLoadGL(); //adding colors

    glViewport(0, 0, 800, 800); // bottom left to top right

    // specify the color of the background
    glClearColor(0.07f, 0.13f, 0.17f, 1.0f); //rgba
    glClear(GL_COLOR_BUFFER_BIT);
    glfwSwapBuffers(window);

    while (!glfwWindowShouldClose(window)) // we add this because when we create the window it closes in a split second to prevent that we tell glfw to wait till we press the quit button
    {
        glfwPollEvents(); // tell glfw to process the window resize etc
    }

    glfwDestroyWindow(window);
    glfwTerminate();

    return 0;
}