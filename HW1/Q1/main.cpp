#include <iostream>
#include <sstream>
#include <iomanip>
#include <cstdlib>
#include <cstdio>
#include <vector>
#include "image.h"
//#include "color.h"
//#include "mesh.h"

using namespace std;

#define NUM_DEBUG_COLLAPSES 10
#define WHITE Color(255,255,255)

int findCost(Color x, Color y) {
  int cost = abs(x.r - y.r) + abs(x.g - y.g) + abs(x.b - y.b);
  //cout << "pixel 1: " << x.r << " " << c1.g << " " << c1.b << endl;
  //cout << "pixel 2: " << c2.r << " " << c2.g << " " << c2.b << endl;
  return cost;
}

int main(int argc, char* argv[]) {

  // default values
  int rows = 10;
  int cols = 10;
  std::string source = "dog.ppm";
  std::string target = "beach.ppm";
  std::string mask = "mask1.ppm";
  Image image, image2, image3;
  image.Load(source);
  image2.Load(target);
  image3.Load(mask);

  Image output;
  output.Load("output.ppm");
  bool blend = false;
  if (argv[1] == "-b") {
    blend = true;
  }

  //cout << cutoff << endl;
  //cout << image.Height() << endl;
  //Color test = image.GetPixel(651,750);
  //cout << test.r << " " << test.g << " " << test.b << endl;
  //cout << findCost(image, 1079, 696) << endl;
  //cout << findCost(image, 0, 1079) << endl;
  vector<vector<Color>> data;
  vector<vector<Color>> data2;
  vector<vector<Color>> data3;

  for (int i = 0; i < image.Width(); i++) {
    vector<Color> row;
    vector<Color> row2;
    vector<Color> row3;
    for (int j = 0; j < image.Height(); j++) {
      row.push_back(image.GetPixel(i,j));
      row2.push_back(image2.GetPixel(i,j));
      row3.push_back(image3.GetPixel(i,j));
    }
    data.push_back(row);
    data2.push_back(row2);
    data3.push_back(row3);
  }

  //for (int i = 0; i < data.size(); i++) {
  //  cout << data[i][0].r << endl;
  //}
  cout << data.size() << " " << data[0].size() << endl;
  
  //vector<int> row;
  
  for (int j = 0; j < image.Height(); j++) {
    
    
    for (int i = 0; i < image.Width()-1; i++) {
      Color msk = data3[i][j];
      if ((msk.r + msk.g + msk.b) / 3 == 255) {
        output.SetPixel(i,j,data[i][j]);
      }
      else output.SetPixel(i,j,data2[i][j]);
    }   
    
  }

  output.Save("output.ppm");
  

  //cout << min << " " << fx << endl;
  

  
}
