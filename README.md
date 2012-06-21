**CNCAngularRotate** (cncangrot) is a G-code translation utility sporting angular rotation about any axis in radians or degrees.
This command was written to speed up production of a product comprised of an assembly repeated around (0,0); because of the
assumptions made in writing this utility, I can only recommend it for a Milltronics MV16 CNC machine. By no means should
you use this utility in production without double checking the output to see if it corrisponds with your machine's needs.
However, a relieving factor should be noted that this utility only operates on `G00` and `G01` and therefore will not alter
vertical height (ie, no slamming of bits).

## Dependancies
* Python 2.7 -or- 3+