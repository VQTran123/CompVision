#ifndef _COLOR_H_
#define _COLOR_H_

class Color {
public:
  Color(int r_=255, int g_=255, int b_=255) : r(r_),g(g_),b(b_) {}
  bool isWhite() const { return r==255 && g==255 && b==255; }
  bool isBlack() const { return r==0 && g==0 && b==0; }
  int r,g,b;

  Color Average(const Color &a, const Color &b) {
    float r_ = (a.r + b.r) / 2.0;
    float g_ = (a.g + b.g) / 2.0;
    float b_ = (a.b + b.b) / 2.0;
    return Color(r_,g_,b_);
  }

};

#endif