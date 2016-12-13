close all
load('magDumpNOCAL.txt');

AxisLim = 6000;

figure(1)

xNOCAL = magDumpNOCAL(:, 1); yNOCAL = magDumpNOCAL(:,2); zNOCAL = magDumpNOCAL(:,3);
scatter3 (xNOCAL(:), yNOCAL(:), zNOCAL(:), 4, zNOCAL(:), 'filled');
xlim([-AxisLim AxisLim]);
ylim([-AxisLim AxisLim]);
zlim([-AxisLim AxisLim]);
xlabel('X');
ylabel('Y');
zlabel('Z');
title('NOCAL')
hold on

xNOCAL_min = min(xNOCAL);
yNOCAL_min = min(yNOCAL);
zNOCAL_min = min(zNOCAL);

xNOCAL_max = max(xNOCAL);
yNOCAL_max = max(yNOCAL);
zNOCAL_max = max(zNOCAL);


middleNOCAL = [(xNOCAL_min + xNOCAL_max)/2, (yNOCAL_min + yNOCAL_max)/2, (zNOCAL_min + zNOCAL_max)/2];
scatter3(middleNOCAL(:,1), middleNOCAL(:,2), middleNOCAL(:,3), 4, [0.4, 1, 0.4], '*');
txt1 = '\leftarrow middle point';
% text(x3,y3,txt3,'HorizontalAlignment','right')

meanNOCAL = mean(magDumpNOCAL);
scatter3(meanNOCAL(:,1), meanNOCAL(:,2), meanNOCAL(:,3), 4, [1, 0.4, 0.4], 's');
txt2 = '\leftarrow middle point';


print -dpng 'imgs/nocal.png'
view([0 0])
print -dpng 'imgs/nocal_XY.png'
view([90 0])
print -dpng 'imgs/nocal_XZ.png'
view([0 90])
print -dpng 'imgs/nocal_YZ.png'

figure(2)

load('magDumpCAL.txt');
xCAL = magDumpCAL(:, 1); yCAL = magDumpCAL(:,2); zCAL = magDumpCAL(:,3);
scatter3 (xCAL(:), yCAL(:), zCAL(:), 4, zCAL(:), 'filled');
xlim([-AxisLim AxisLim]);
ylim([-AxisLim AxisLim]);
zlim([-AxisLim AxisLim]);
xlabel('X');
ylabel('Y');
zlabel('Z');
title('CAL')

xCAL_min = min(xCAL);
yCAL_min = min(yCAL);
zCAL_min = min(zCAL);

xCAL_max = max(xCAL);
yCAL_max = max(yCAL);
zCAL_max = max(zCAL);

print -dpng 'imgs/cal.png'
view([0 0])
print -dpng 'imgs/cal_XZ.png'
view([90 0])
print -dpng 'imgs/cal_YZ.png'
view([0 90])
print -dpng 'imgs/cal_XY.png'

printf('%020s: %04s:%05d, %04s:%05d, %04s:%05d, %04s:%05d, %04s:%05d, %04s:%05d \r\n',
       'NOCAL',
       'xmin',
       xNOCAL_min,
       'xmax',
       xNOCAL_max,
       'ymin',
       yNOCAL_min,
       'ymax',
       yNOCAL_max,
       'zmin',
       zNOCAL_min,
       'zmax',
       zNOCAL_max
       );

printf('%20s: %04s:%05.3f, %04s:%05.3f, %04s:%05.3f \r\n',
       'Cal values',
       'x',
       (xNOCAL_min + xNOCAL_max)/2,
       'y',
       (yNOCAL_min + yNOCAL_max)/2,
       'z',
       (zNOCAL_min + zNOCAL_max)/2
       );

printf('%20s: %04s:%05.3f, %04s:%05.3f, %04s:%05.3f \r\n',
       'Offset after CAL',
       'x',
       (xCAL_min + xCAL_max)/2,
       'y',
       (yCAL_min + yCAL_max)/2,
       'z',
       (zCAL_min + zCAL_max)/2
       );

% useless because it depends on how someone wiggles the sensor during data
% dumping. method above (average of min and max) works best when you have
% regular sphere (which I do have now)
% printf('%20s: %04s:%05.3f, %04s:%05d, %04s:%05d \r\n',
%        'Mean of NOCAL',
%        'x',
%        meanNOCAL(:,1),
%        'y',
%        meanNOCAL(:,2),
%        'z',
%        meanNOCAL(:,3)
%        );
