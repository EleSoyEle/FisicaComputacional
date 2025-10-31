  #include "colors.inc"
  background { color White }
  camera {
    location <0, 0,10>
    look_at  <10, -2,  0>
  }
  sphere {
    <10, 1, 0>, 1
    texture {
      pigment { color Yellow }
    }
  }
  box {
    <5,2,0>,
    <3,-1,-1>
    texture {
        pigment {color Blue}
    }
  }
    cone {
    <6, 2, 0>, 0.3
    <8, 2, 0>, 1.0
    texture { 
        pigment {color Cyan}
    }
  }
  plane { <0, 1, 0>, -1
    texture {
        pigment { color Red }
    }
  }
  torus {
    1.0, 0.5 // Radio Mayor, Radio Menor

    pigment { color Blue }
    rotate <90, 0, 0>
    translate <10, 0, 4>
}
  cylinder {
    <10, 0, 7>,     
    <9, 0, 6>,     
    0.5
    texture { 
        pigment {color Green}
     }
  }
  light_source { <2, 4, -3> color White}