module mux4(din,sel,out);
    input [3:0] din;
    input [1:0] sel;
    output out;

    wire s1n,s0n;
    wire y0,y1,y2,y3;

    not (s1n,sel[1]);
    not (s0n,sel[0]);

    and (y0,din[0],s1n,s0n);
    and (y1,din[1],s1n,sel[0]);
    and (y2,din[2],sel[1],s0n);
    and (y3,din[3],sel[1],sel[0]);

    or (out,y0,y1,y2,y3);
endmodule