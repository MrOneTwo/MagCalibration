function [ret1, ret2] = go(portNr = 0)

    disp('Starting to capture data in... \n')
    sleep(1)
    disp('3... \n')
    sleep(1)
    disp('2... \n')
    sleep(1)
    disp('1... \n')
    sleep(1)
    disp('GO! \n')

    calibrateMag(portNr)
