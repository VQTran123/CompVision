#include <cstring>
#include <cstdio>
#include "image.h"

// ====================================================================
// ====================================================================
// helper functions for image initialization & image copy

void Image::Allocate(int w, int h) {
  // request enough memory to store the pixels of this image
  width = w;
  height = h;
  delete [] data;
  if (width == 0 && height == 0) {
    data = NULL;
  } else {
    assert (width > 0 && height > 0);
    data = new Color[width*height]; 
  }
}

void Image::CopyHelper(const Image &image) {
  Allocate (image.Width(), image.Height());
  for (int i = 0; i < image.Width(); i++) {
    for (int j = 0; j < image.Height(); j++) {
      this->SetPixel(i,j,image.GetPixel(i,j));
    }
  }
}

// ====================================================================
// ====================================================================

bool Image::Save(const std::string &filename) const {
  int len = filename.length();
  if (!(len > 4 && filename.substr(len-4) == std::string(".ppm"))) {
    std::cerr << "ERROR: This is not a PPM filename: " << filename << std::endl;
    return false;
  }
  FILE *file = fopen(filename.c_str(), "wb");
  if (file == NULL) {
    std::cerr << "Unable to open " << filename << " for writing\n";
    return false;
  }

  // misc header information
  fprintf (file, "P6\n");
  fprintf (file, "%d %d\n", width,height);
  fprintf (file, "255\n");

  // the data
  // flip y so that (0,0) is bottom left corner
  for (int y = height-1; y >= 0; y--) {
    for (int x=0; x<width; x++) {
      Color v = GetPixel(x,y);
      fputc ((unsigned char)(v.r),file);
      fputc ((unsigned char)(v.g),file);
      fputc ((unsigned char)(v.b),file);
    }
  }
  fclose(file);
  return true;
}


bool Image::Load(const std::string &filename) {
  int len = filename.length();
  if (!(len > 4 && filename.substr(len-4) == std::string(".ppm"))) {
    std::cerr << "ERROR: This is not a PPM filename: " << filename << std::endl;
    return false;
  }
  FILE *file = fopen(filename.c_str(),"rb");
  if (file == NULL) {
    std::cerr << "Unable to open " << filename << " for reading\n";
    return false;
  }

  //width = 1920;
  //height = 1080;

  // misc header information
  char tmp[100];
  fgets(tmp,100,file); 
  assert (strstr(tmp,"P6"));
  fgets(tmp,100,file); 
  while (tmp[0] == '#') { fgets(tmp,100,file); }
  sscanf(tmp,"%d %d",&width,&height);
  fgets(tmp,100,file); 
  assert (strstr(tmp,"255"));

  // the data
  delete [] data;
  data = new Color[height*width];
  // flip y so that (0,0) is bottom left corner
  for (int y = height-1; y >= 0; y--) {
    for (int x = 0; x < width; x++) {
      Color c;
      c.r = fgetc(file);
      c.g = fgetc(file);
      c.b = fgetc(file);
      SetPixel(x,y,c);
    }
  }
  fclose(file);
  return true;
}

// ====================================================================
// ====================================================================

