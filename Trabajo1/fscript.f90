program hola
implicit none

integer :: i,p,pt,pc
real :: x,y,xn,yn,r
Call random_seed

pt = 1000
p = 0
do i=1,pt
    call random_number(x)
    call random_number(y)
    xn = 2*x-1
    yn = 2*y-1
    r = xn*xn+yn*yn
    print*, r
    if (r  .le. 1) then
        p = p+1
    end if
end do

pc = p/pt
Print *, 4*pc
end program hola