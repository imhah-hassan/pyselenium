pip3 install ddt 

pip3 install selenium 

pip3 install behave

pip3 install Faker



pip3 install allure-behave
behave -f allure_behave.formatter:AllureFormatter -o ./results ./features

download allure-2.7.0.zip unzip into c:\apps
SET PATH=C:\Apps\allure\bin;%PATH%
allure serve ./results