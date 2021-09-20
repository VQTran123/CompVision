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
  std::string name = "image1.ppm";
  std::string name2 = "image2.ppm";
  std::string name3 = "image3.ppm";
  Image image, image2, image3;
  image.Load(name2);
  image2.Load(name);
  image3.Load(name3);

  int cutoff = stoi(argv[1]);
  int cutoff2 = stoi(argv[2]);
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
  Color red(255,0,0);
  for (int j = 0; j < image.Height(); j++) {
    int min = 1000;
    int fx = 0;
    for (int i = cutoff; i < image.Width()-1; i++) {
      int fx_ = findCost(data[i][j], data[i+1][j]);
      if (fx_ < min) {
        min = fx_;
        //cout << min << endl;
        fx = i;
      }
      //row.push_back();
      //if (i % 100 == 0) cout << i << endl;
    }
    cout << "min cut at row " << j << " = " << fx << endl;
    //image.SetPixel(fx,j,red);
    for (int i = fx; i < image.Width()-1; i++) {
      image.SetPixel(i,j,image2.GetPixel(i,j));
    }
  }

  for (int j = 0; j < image.Height(); j++) {
    int min = 1000;
    int fx = 0;
    for (int i = cutoff2; i < image.Width()-1; i++) {
      int fx_ = findCost(data[i][j], data[i+1][j]);
      if (fx_ < min) {
        min = fx_;
        //cout << min << endl;
        fx = i;
      }
      //row.push_back();
      //if (i % 100 == 0) cout << i << endl;
    }
    cout << "min cut at row " << j << " = " << fx << endl;
    //image.SetPixel(fx,j,red);
    for (int i = fx; i < image.Width()-1; i++) {
      image.SetPixel(i,j,image3.GetPixel(i,j));
    }
  }

  image.Save(name);
  

  //cout << min << " " << fx << endl;
  

  
}
