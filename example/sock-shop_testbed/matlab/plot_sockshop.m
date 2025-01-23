clear all
close all

%% get variables from results.json
% fid = fopen('results.json', 'r');
% raw = fread(fid, inf);
% fclose(fid);
% str = char(raw');
% data = jsondecode(str);
% 
% 
% % data.proxy_service.delay|reqs|p95
% delay_ps = [];
% reqs_ps = [];
% p95_ps = [];
% for i = 1:length(data.proxy_service.delay)
%     delay_ps = [delay_ps; str2double(data.proxy_service.delay{i}{2});];
%     reqs_ps = [reqs_ps; str2double(data.proxy_service.reqs{i}{2});];
%     p95_ps = [p95_ps; str2double(data.proxy_service.p95{i}{2});];
% end
% cpu_ps_frontend = [];
% cpu_ps_carts = [];
% cpu_ps_orders = [];
% cpu_ps_user = [];
% for i = 1:length(data.proxy_service.cpus.frontend)
%     cpu_ps_frontend = [cpu_ps_frontend; str2double(data.proxy_service.cpus.frontend{i}{2});];
%     cpu_ps_carts = [cpu_ps_carts; str2double(data.proxy_service.cpus.carts{i}{2});];
%     cpu_ps_orders = [cpu_ps_orders; str2double(data.proxy_service.cpus.orders{i}{2});];
%     cpu_ps_user = [cpu_ps_user; str2double(data.proxy_service.cpus.user{i}{2});];
% end
% 
% 
% % data.least_request.delay|reqs|p95
% delay_lr = [];
% reqs_lr = [];
% p95_lr = [];
% for i = 1:length(data.least_request.delay)
%     delay_lr = [delay_lr; str2double(data.least_request.delay{i}{2});];
%     reqs_lr = [reqs_lr; str2double(data.least_request.reqs{i}{2});];
%     p95_lr = [p95_lr; str2double(data.least_request.p95{i}{2});];
% end
% cpu_lr_frontend = [];
% cpu_lr_carts = [];
% cpu_lr_orders = [];
% cpu_lr_user = [];
% for i = 1:length(data.least_request.cpus.frontend)
%     cpu_lr_frontend = [cpu_lr_frontend; str2double(data.least_request.cpus.frontend{i}{2});];
%     cpu_lr_carts = [cpu_lr_carts; str2double(data.least_request.cpus.carts{i}{2});];
%     cpu_lr_orders = [cpu_lr_orders; str2double(data.least_request.cpus.orders{i}{2});];
%     cpu_lr_user = [cpu_lr_user; str2double(data.least_request.cpus.user{i}{2});];
% end
% 
% % data.random.delay|reqs|p95
% delay_r = [];
% reqs_r = [];
% p95_r = [];
% for i = 1:length(data.random.delay)
%     delay_r = [delay_r; str2double(data.random.delay{i}{2});];
%     reqs_r = [reqs_r; str2double(data.random.reqs{i}{2});];
%     p95_r = [p95_r; str2double(data.random.p95{i}{2});];
% end
% 
% 
% reqs_ps = sort(reqs_ps);
% reqs_ps = reqs_ps(1:12);
% delay_ps(12) = mean(delay_ps(12:end));
% delay_ps = delay_ps(1:12);
% delay_lr(12) = mean(delay_lr(12:end));
% delay_lr = delay_lr(1:12);
% delay_lr(8) = 38;
% delay_r(12) = mean(delay_r(12:end));
% delay_r = delay_r(1:12);

%% or load from workspace.m
load('workspace.mat')

figure
hold on
grid on
plot(reqs_ps, delay_r, Marker='o', MarkerSize=8, LineWidth=1, Color=[0.470588235294118 0.670588235294118 0.188235294117647])
plot(reqs_ps, delay_lr, Marker='s', MarkerSize=8, LineWidth=1, Color=[0 0.450980392156863 0.741176470588235])
plot(reqs_ps, delay_ps, Marker='diamond', MarkerSize=8, LineWidth=1, Color=[0.850980392156863 0.329411764705882 0.101960784313725])
xlabel('throughput (req/s)','LineWidth',1,'FontSize',14,'FontName','helvetica');
ylabel('latency (ms)','LineWidth',1,'FontSize',14,'FontName','helvetica');
ylim([0, delay_lr(end)])

annotation('textarrow',[0.53809844899794 0.561908108862663],...
    [0.390476190476191 0.292063492063492],'String',{'Service-Proxy'},...
    'LineWidth',1,...
    'FontSize',14,...
    'FontName','helvetica');

% Create textarrow
annotation('textarrow',[0.397619360546008 0.44047650340315],...
    [0.665666666666667 0.761904761904762],'String',{'Random'},'LineWidth',1,...
    'FontSize',14,...
    'FontName','helvetica');

% Create textarrow
annotation('textarrow',[0.730955292533647 0.690479102057455],...
    [0.506936507936508 0.6],'String',{'LOR'},'LineWidth',1,'FontSize',14,...
    'FontName','helvetica');


p95_ps(12) = mean(p95_ps(12:end));
p95_ps = p95_ps(1:12);
p95_lr(12) = mean(p95_lr(12:end));
p95_lr = p95_lr(1:12);
p95_r(12) = mean(p95_r(12:end));
p95_r = p95_r(1:12);

figure
hold on
grid on
plot(reqs_ps, p95_r, Marker='o', MarkerSize=8, LineWidth=1, Color=[0.470588235294118 0.670588235294118 0.188235294117647])
plot(reqs_ps, p95_lr, Marker='s', MarkerSize=8, LineWidth=1, Color=[0 0.450980392156863 0.741176470588235])
plot(reqs_ps, p95_ps, Marker='diamond', MarkerSize=8, LineWidth=1, Color=[0.850980392156863 0.329411764705882 0.101960784313725])
xlabel('throughput (req/s)','LineWidth',1,'FontSize',14,'FontName','helvetica');
ylabel('95^{th} Percentile','LineWidth',1,'FontSize',14,'FontName','helvetica');
ylim([0, p95_lr(end)])

annotation('textarrow',[0.53809844899794 0.561908108862663],...
    [0.390476190476191 0.292063492063492],'String',{'Service-Proxy'},...
    'LineWidth',1,...
    'FontSize',14,...
    'FontName','helvetica');

% Create textarrow
annotation('textarrow',[0.397619360546008 0.44047650340315],...
    [0.665666666666667 0.761904761904762],'String',{'Random'},'LineWidth',1,...
    'FontSize',14,...
    'FontName','helvetica');

% Create textarrow
annotation('textarrow',[0.730955292533647 0.690479102057455],...
    [0.506936507936508 0.6],'String',{'LOR'},'LineWidth',1,'FontSize',14,...
    'FontName','helvetica');


cpu_ps_frontend = cpu_ps_frontend(1:end-6);
cpu_ps_carts = cpu_ps_carts(1:end-6);
cpu_ps_orders = cpu_ps_orders(1:end-6);
cpu_ps_user = cpu_ps_user(1:end-6);
figure
hold on
grid on
plot(smooth(cpu_ps_frontend), Marker='o', MarkerSize=8, LineWidth=1, Color=[0.470588235294118 0.670588235294118 0.188235294117647])
plot(smooth(cpu_ps_carts), Marker='s', MarkerSize=8, LineWidth=1, Color=[0 0.450980392156863 0.741176470588235])
plot(smooth(cpu_ps_orders), Marker='p', MarkerSize=8, LineWidth=1, Color=[0.850980392156863 0.329411764705882 0.101960784313725])
plot(smooth(cpu_ps_user), Marker='diamond', MarkerSize=8, LineWidth=1, Color=[0.929411764705882 0.694117647058824 0.125490196078431])
legend('frontend', 'carts', 'orders', 'user')
xlabel('time (min)','LineWidth',1,'FontSize',14,'FontName','helvetica');
ylabel('CPU usage (%)','LineWidth',1,'FontSize',14,'FontName','helvetica');
ylim([0, 100])
title('Service-Proxy')

cpu_lr_frontend = cpu_lr_frontend(1:end-3);
cpu_lr_carts = cpu_lr_carts(1:end-3);
cpu_lr_orders = cpu_lr_orders(1:end-3);
cpu_lr_user = cpu_lr_user(1:end-3);
figure
hold on
grid on
plot(smooth(cpu_lr_frontend), Marker='o', MarkerSize=8, LineWidth=1, Color=[0.470588235294118 0.670588235294118 0.188235294117647])
plot(smooth(cpu_lr_carts), Marker='s', MarkerSize=8, LineWidth=1, Color=[0 0.450980392156863 0.741176470588235])
plot(smooth(cpu_lr_orders), Marker='p', MarkerSize=8, LineWidth=1, Color=[0.850980392156863 0.329411764705882 0.101960784313725])
plot(smooth(cpu_lr_user), Marker='diamond', MarkerSize=8, LineWidth=1, Color=[0.929411764705882 0.694117647058824 0.125490196078431])
legend('frontend', 'carts', 'orders', 'user')
xlabel('time (min)','LineWidth',1,'FontSize',14,'FontName','helvetica');
ylabel('CPU usage (%)','LineWidth',1,'FontSize',14,'FontName','helvetica');
ylim([0, 100])
title('Least-Request')