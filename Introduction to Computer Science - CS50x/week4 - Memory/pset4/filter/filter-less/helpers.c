#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float avg = ((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = round(avg);
            image[i][j].rgbtGreen = round(avg);
            image[i][j].rgbtRed = round(avg);
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float sepiaRed = ((0.393 * image[i][j].rgbtRed) + (0.769 * image[i][j].rgbtGreen) + (0.189 * image[i][j].rgbtBlue));
            float sepiaGreen = ((0.349 * image[i][j].rgbtRed) + (0.686 * image[i][j].rgbtGreen) + (0.168 * image[i][j].rgbtBlue));
            float sepiaBlue = ((0.272 * image[i][j].rgbtRed) + (0.534 * image[i][j].rgbtGreen) + (0.131 * image[i][j].rgbtBlue));
            image[i][j].rgbtBlue = fmin(255, round(sepiaBlue));
            image[i][j].rgbtGreen = fmin(255, round(sepiaGreen));
            image[i][j].rgbtRed = fmin(255, round(sepiaRed));
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    void swap(RGBTRIPLE *, RGBTRIPLE *);
    int half = (width / 2);
    if (half < 1)
    {
        return;
    }
    if ((width % 2) == 0)
    {
        for (int i = 0; i < height; i++)
        {
            for (int j = 0; j < half + 1; j++)
            {
                swap(&image[i][j], &image[i][width - 1 - j]);
            }
        }
    }
    else
    {
        for (int i = 0; i < height; i++)
        {
            for (int j = 0; j < half; j++)
            {
                swap(&image[i][j], &image[i][width - 1 - j]);
            }
        }
    }
    return;
}

void swap(RGBTRIPLE *image1, RGBTRIPLE *image2)
{
    RGBTRIPLE thrdimage;
    thrdimage = *image1;
    *image1 = *image2;
    *image2 = thrdimage;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    void colors(float, float, float, int, int, RGBTRIPLE *, RGBTRIPLE image[height][width], int, int, int, int, int, int);
    RGBTRIPLE secimage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            secimage[i][j].rgbtBlue = image[i][j].rgbtBlue;
            secimage[i][j].rgbtGreen = image[i][j].rgbtGreen;
            secimage[i][j].rgbtRed = image[i][j].rgbtRed;
        }
    }
    float blue, green, red;
    int countl;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int fboxi = 1;
            int sboxi = 2;
            if (i == 0)
            {
                fboxi = 0;
            }
            if (i == height - 1)
            {
                sboxi = 1;
            }
            int fboxj = 1;
            int sboxj = 2;
            if (j == 0)
            {
                fboxj = 0;
            }
            if (j == width - 1)
            {
                sboxj = 1;
            }
            blue = green = red = 0;
            countl = 0;
            for (int k = i - fboxi; k < i + sboxi; k++)
            {
                for (int l = j - fboxj; l < j + sboxj; l++)
                {
                    blue += secimage[k][l].rgbtBlue;
                    green += secimage[k][l].rgbtGreen;
                    red += secimage[k][l].rgbtRed;
                    countl++;
                }
            }
            float cl = countl;
            blue /= cl;
            green /= cl;
            red /= cl;
            image[i][j].rgbtBlue = (int)round(blue);
            image[i][j].rgbtGreen = (int)round(green);
            image[i][j].rgbtRed = (int)round(red);
        }
    }
    return;
}

