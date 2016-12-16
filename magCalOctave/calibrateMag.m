function [ret1, ret2] = calibrateMag(portNr = 0)
       close all
       samplesCount = 3000

       pkg load instrument-control

       % 3 == errors
       if(exist('serial') != 3)
              disp('No serial support.')
       endif


       serialPort = serial("/dev/ttyUSB0")
       pause(1);

       set(serialPort, 'baudrate', 115200);
       set(serialPort, 'bytesize', 8);
       set(serialPort, 'parity', 'n');
       set(serialPort, 'stopbits', 1);
       set(serialPort, 'timeout', 1); % in seconds

       % inBuffer = srl_read(serialPort, 64);
       notCalibratedData = [];
       inBufferSTR_splitted = {};
       ret1 = [];
       ret2 = [];

       % make sure sensor is in proper mode
       %srl_write(serialPort, "mag\r\n");
       %pause(1);

       while (size(notCalibratedData)(1) != samplesCount)

              inBufferSTR = ReadToTermination(serialPort);
              inBufferSTR_splitted = strsplit(inBufferSTR, ".");
              % disp(inBufferSTR);

              if(size(inBufferSTR_splitted) == [1, 4])
                     if(strcmp(inBufferSTR_splitted{1}, 'MAG') == 0 || strcmp(inBufferSTR_splitted{1}, 'ZMAG') == 0)
                            inBufferNUM(1) = str2double(inBufferSTR_splitted{2});
                            inBufferNUM(2) = str2double(inBufferSTR_splitted{3});
                            inBufferNUM(3) = str2double(inBufferSTR_splitted{4});
                            notCalibratedData = vertcat(notCalibratedData, inBufferNUM);
                     endif
              else
                     disp('not ok data format')
              endif
       endwhile
       fclose(serialPort);

       % disp(notCalibratedData);
       disp('Finished acquiring data.')

       AxisLim = 6000;

       figure(1)

       xNOCAL = notCalibratedData(:, 1); yNOCAL = notCalibratedData(:,2); zNOCAL = notCalibratedData(:,3);
       scatter3 (xNOCAL(:), yNOCAL(:), zNOCAL(:), 4, zNOCAL(:), 'filled');
       xlim([-AxisLim AxisLim]);
       ylim([-AxisLim AxisLim]);
       zlim([-AxisLim AxisLim]);
       xlabel('X');
       ylabel('Y');
       zlabel('Z');
       title('NOCAL')
       daspect ([1 1])
       hold on

       xNOCAL_min = min(xNOCAL);
       yNOCAL_min = min(yNOCAL);
       zNOCAL_min = min(zNOCAL);

       xNOCAL_max = max(xNOCAL);
       yNOCAL_max = max(yNOCAL);
       zNOCAL_max = max(zNOCAL);


       middleNOCAL = [(xNOCAL_min + xNOCAL_max)/2, (yNOCAL_min + yNOCAL_max)/2, (zNOCAL_min + zNOCAL_max)/2];
       scatter3(middleNOCAL(:,1), middleNOCAL(:,2), middleNOCAL(:,3), 4, [0.4, 1, 0.4], '*');

       set(gcf(), "visible", "off")
       print -dpng 'imgs/nocal.png';
       set(gcf(), "visible", "on")
       view([0 0]);
       set(gcf(), "visible", "off")
       print -dpng 'imgs/nocal_XY.png';
       set(gcf(), "visible", "on")
       view([90 0]);
       set(gcf(), "visible", "off")
       print -dpng 'imgs/nocal_XZ.png';
       set(gcf(), "visible", "on")
       view([0 90]);
       set(gcf(), "visible", "off")
       print -dpng 'imgs/nocal_YZ.png';
       set(gcf(), "visible", "on")

       calibratedData = notCalibratedData - middleNOCAL(ones(size(notCalibratedData,1),1),:);
       figure(2)

       xCAL = calibratedData(:, 1); yCAL = calibratedData(:,2); zCAL = calibratedData(:,3);
       scatter3 (xCAL(:), yCAL(:), zCAL(:), 4, zCAL(:), 'filled');
       xlim([-AxisLim AxisLim]);
       ylim([-AxisLim AxisLim]);
       zlim([-AxisLim AxisLim]);
       xlabel('X');
       ylabel('Y');
       zlabel('Z');
       title('CAL')
       daspect ([1 1])
       hold on

       % xCAL_min = min(xCAL);
       % yCAL_min = min(yCAL);
       % zCAL_min = min(zCAL);

       % xCAL_max = max(xCAL);
       % yCAL_max = max(yCAL);
       % zCAL_max = max(zCAL);

       set(gcf(), "visible", "off")
       print -dpng 'imgs/cal.png';
       set(gcf(), "visible", "on")
       view([0 0]);
       set(gcf(), "visible", "off")
       print -dpng 'imgs/cal_XZ.png';
       set(gcf(), "visible", "on")
       view([90 0]);
       set(gcf(), "visible", "off")
       print -dpng 'imgs/cal_YZ.png';
       set(gcf(), "visible", "on")
       view([0 90]);
       set(gcf(), "visible", "off")
       print -dpng 'imgs/cal_XY.png';
       set(gcf(), "visible", "on")

       % printf('%020s: %04s:%05d, %04s:%05d, %04s:%05d, %04s:%05d, %04s:%05d, %04s:%05d \r\n',
       %        'NOCAL',
       %        'xmin',
       %        xNOCAL_min,
       %        'xmax',
       %        xNOCAL_max,
       %        'ymin',
       %        yNOCAL_min,
       %        'ymax',
       %        yNOCAL_max,
       %        'zmin',
       %        zNOCAL_min,
       %        'zmax',
       %        zNOCAL_max
       %        );

       printf('%20s: %04s:%05.3f, %04s:%05.3f, %04s:%05.3f \r\n',
              'Cal values',
              'x',
              (xNOCAL_min + xNOCAL_max)/2,
              'y',
              (yNOCAL_min + yNOCAL_max)/2,
              'z',
              (zNOCAL_min + zNOCAL_max)/2
              );

       printf('%.6s[%08d,%08d,%08d] \r\n',
              '=zmag=',
              -1 * round((xNOCAL_min + xNOCAL_max)/2),
              -1 * round((yNOCAL_min + yNOCAL_max)/2),
              -1 * round((zNOCAL_min + zNOCAL_max)/2)
              );

       % printf('%20s: %04s:%05.3f, %04s:%05.3f, %04s:%05.3f \r\n',
       %        'Offset after CAL',
       %        'x',
       %        (xCAL_min + xCAL_max)/2,
       %        'y',
       %        (yCAL_min + yCAL_max)/2,
       %        'z',
       %        (zCAL_min + zCAL_max)/2
       %        );

       ret1 = notCalibratedData;
       ret2 = middleNOCAL;
end

function [char_array] = ReadToTermination (srl_handle, term_char)

    % parameter term_char is optional, if not specified
    % then CR = '\r' = 13dec is the default.
if(nargin == 1)
  term_char = 13;
end

not_terminated = true;
i = 1;
int_array = uint8(1);

while not_terminated

    val = srl_read(srl_handle, 1);

    if(val == term_char)
        not_terminated = false;
    end

  % Add char received to array
  int_array(i) = val;
  i = i + 1;

end

  % Change int array to a char array and return a string array
  char_array = char(int_array);

endfunction
