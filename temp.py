clear;close all;clc
%% 原始信息
%导入data.mat矩阵作为原始信息，fs是原始采样率
load data.mat
x = x_upconv';
fs = 16e6;
base = 2 ^ 10;
Inputdata=x(1:32 * base);%选取一部分作为输入
figure();
df = -fs/2:fs/(32 * base): fs / 2 - 1; %频谱横坐标
plot(df, 20 * log10(abs(fftshift(fft(Inputdata)))), 'r');title('Fig1 原始采样信号频谱');
%% 正交变换
%原中频：
f0=2e6;
%I路:
Idata= Inputdata. * cos(2 * pi * f0 * (1:32*base) / fs);
%Q路：
Qdata= Inputdata. * sin(2 * pi * f0 * (1:32*base) / fs);
%画出I/Q路的频域图
figure();
subplot(1,2,1);
plot(df,20*log10(abs(fftshift(fft(Idata)))),'r');title('正交变换I路频谱');
subplot(1,2,2)
plot(df,20*log10(abs(fftshift(fft(Qdata)))),'r');title('正交变换Q路频谱');
%% 滤波器参数设计
%%%应用fdatool生成如下滤波器
%第一级：CIC：3级CIC滤波器（5倍抽取）fs=16Mhz
%第二级：HB1：fpass=20kHz fs=3200kHz
%第三级：HB2：fpass=20kHz fs=1600kHz
%第四级：HB3：fpass=20kHz fs=800kHz
%第五级：Fir：fpass=20kHz fstop=40kHz fs=400kHz
%查看滤波器级联曲线
%fvtool(cascade(CIC,HB1,HB2,HB3,Fir),'Fs',fs,'ShowReference', 'off');
%查看设计滤波器频谱
fvtool(CIC,'Fs',16e6,'ShowReference','off');
fvtool(HB1,'Fs',3200e3,'ShowReference','off');
fvtool(HB2,'Fs',1600e3,'ShowReference','off');
fvtool(HB3,'Fs',800e3,'ShowReference','off');
fvtool(Fir,'Fs',400e3,'ShowReference','off');
%创建BA两个cell型号变量来保存滤波器系数
B=cell(5,1);A=cell(5,1);
[b,a]=tf(CIC);B{1}=b;A{1}=a;
[b,a]=tf(HB1);B{2}=b;A{2}=a;
[b,a]=tf(HB2);B{3}=b;A{3}=a;
[b,a]=tf(HB3);B{4}=b;A{4}=a;
[b,a]=tf(Fir);B{5}=b;A{5}=a;
%D矩阵用来存储抽样间距
D=[5 2 2 2 4];
%% I/Q路滤波
%初始化I/Q值
Idata_tmp=Idata;
Qdata_tmp=Qdata;
for m=1:5
    %滤波：
    Idata_tmp=filter(B{m},A{m},Idata_tmp);
    Qdata_tmp=filter(B{m},A{m},Qdata_tmp);
    %抽样：
    Idata_tmp=Idata_tmp(1:D(m):end);
    Qdata_tmp=Qdata_tmp(1:D(m):end);
end
%赋值最终输出
Idata_out=Idata_tmp;
Qdata_out=Qdata_tmp;
%% 抽样滤波后的I/Q路信号频谱图
%抽样滤波后得到I路Q路信号，采样率变为100kHz
fs_new=100e3;%抽样滤波后的采样率变为100k
df_new=linspace(-fs_new/2,fs_new/2,length(Idata_out));
figure();
subplot(1,2,1);
plot(df_new,20*log10(abs(fftshift(fft(Idata_out)))),'r');title('抽样滤波后正交变换I路频谱');
subplot(1,2,2)
plot(df_new,20*log10(abs(fftshift(fft(Qdata_out)))),'r');title('抽样滤波后正交变换Q路频谱');
% figure();
% %Odata=sqrt(Idata_5.^2+Qdata_5.^2);
% Odata=Idata_out+1j*Qdata_out;
% plot(df_new,20*log10(abs(fftshift(fft(Odata)))),'r');title('抽样滤波后正交变换Q路频谱');
