pip install selenium   
pip install xmlrunner   

pip install ddt   


pip install behave  


pip install Faker  
 





pip install allure-behave   

behave -f allure_behave.formatter:AllureFormatter -o ./results ./features  


download allure-2.20.1.zip unzip into c:\apps  
https://github.com/allure-framework/allure2/releases/download/2.20.1/allure-2.20.1.zip   

SET PATH=C:\Apps\allure\bin;%PATH%  
allure serve ./results  