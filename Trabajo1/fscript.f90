program Pi
implicit none

integer :: i,p,pt
real :: x,y,xn,yn,r,pc
Call random_seed

pt = 100000
p = 0
do i=1,pt
    call random_number(x)
    call random_number(y)
    xn = 2*x-1
    yn = 2*y-1
    r = xn*xn+yn*yn
    if (r  .le. 1) then
        p = p+1
    end if
end do

pc = real(p)/real(pt)
Print *, 4*pc
end program Pi