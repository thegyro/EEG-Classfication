% eye_in - 3*240 matrix 3 features,240 samples,first 120 columns denote blink,next 120 columns Non-Blink

% eye_target - 2*240 matrix 2 classes - first 120 columns transpose([1,0])
% denote class blink, next 120 columns transpose([0,1]) denote class non blink

% clench_in and clench_target are defined similarly

% Feed Forwrd Neural Network Blink Classification
eye_net = feedforwardnet([30,15]);
eye_net = configure(eye_net, eye_in, eye_target);
[eye_net,eye_tr] = train(eye_net, eye_in, eye_target);

eye_output = eye_net(eye_in);
eye_train = eye_target.*eye_tr.trainMask{1};
eye_test = eye_target.*eye_tr.testMask{1};
eye_val = eye_target.*eye_tr.valMask{1};

plotperform(eye_tr);
plotconfusion(eye_train,eye_output,'Train',eye_val,eye_output,'Validation',eye_test,eye_output,'Testing',eye_target,eye_output,'Overall');