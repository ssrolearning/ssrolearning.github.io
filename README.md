## 가상환경에서 실행

python main.py

## 도커에서 실행

태그이름 todayassi-demo

docker-compose.yml
Dockerfile
gunicorn.conf.py
requirements.txt
startup.sh

도커빌드 
docker build --tag todayassi-demo .
도커실행 
docker run --detach --publish 3100:3100 todayassi-demo
도커서비스접속
http://localhost:3100/

지우고재시작할때
lsof -i :3100
kill -9 [PID]

## 애저에서 실행

애저로그인
az login --scope https://management.core.windows.net//.default
az login --tenant eeacc0eb-14ef-4a37-b43c-eb5847b81fcf

AZ 리소스그룹 생성 (web-app-todayassi-rg)
az group create --name web-app-todayassi-rg --location eastus

AZ 컨테이너 레지스트리(ACR - Azure Container Registry) 생성 (todayassiacr)
az acr create --resource-group web-app-todayassi-rg --name todayassiacr --sku Basic --admin-enabled true

AZ ACR 비번 알아내기
ACR_PASSWORD=$(az acr credential show --resource-group web-app-todayassi-rg --name todayassiacr --query "passwords[?name == 'password'].value" --output tsv)

AZ ACR 비번 출력하기
echo $ACR_PASSWORD

AZ ACR 이미지 빌드
az acr build --resource-group web-app-todayassi-rg --registry todayassiacr --image webapptodayassi:latest0015 .

삭제
az webapp delete --name todayassi --resource-group web-app-todayassi-rg

웹 배포
az webapp create --resource-group web-app-todayassi-rg --plan webplan --name todayassi --docker-registry-server-password $ACR_PASSWORD --docker-registry-server-user todayassiacr --role acrpull --deployment-container-image-name todayassiacr.azurecr.io/webapptodayassi:latest0015

웹접속
todayassi.azurewebsites.net

로그 설정 활성화: 먼저, 웹 앱에 대한 로깅을 활성화해야 합니다. 다음 명령을 사용하여 로깅을 활성화할 수 있습니다:
az webapp log config --name todayassi --resource-group web-app-todayassi-rg --docker-container-logging filesystem

로그 실시간 모니터링: 로그가 활성화되면, 다음 명령을 사용하여 실시간으로 로그를 모니터링할 수 있습니다:
az webapp log tail --name todayassi --resource-group web-app-todayassi-rg


:( Application Error
If you are the application administrator, you can access the diagnostic resources.


웹서버 컨테이너화: 웹서버는 도커 컨테이너로 배포됩니다. 이 컨테이너는 애플리케이션 코드와 필요한 웹서버 환경(예: Apache, Nginx)을 포함합니다. 도커 이미지를 생성하고 Azure Container Registry에 업로드합니다.

별도의 데이터베이스 서비스 사용: 데이터베이스는 컨테이너 내부에 저장하지 않고 Azure의 관리형 데이터베이스 서비스(예: Azure SQL Database, Azure Cosmos DB)를 사용합니다. 이렇게 하면 데이터베이스가 웹서버와 독립적으로 운영되어, 웹서버 컨테이너를 재배포해도 데이터가 유지됩니다.

지속적인 데이터 저장을 위한 볼륨 사용: 웹서버에서 생성되는 로그나 업로드된 파일과 같은 데이터를 위해 Azure File Storage 또는 Azure Blob Storage와 같은 외부 저장소를 사용합니다. 도커에서는 이러한 저장소를 볼륨으로 마운트하여 데이터의 지속성을 보장합니다.

서비스 오케스트레이션: 여러 컨테이너를 관리하기 위해 Azure Kubernetes Service(AKS) 또는 Azure Container Instances(ACI) 같은 오케스트레이션 서비스를 사용할 수 있습니다. 이를 통해 자동 확장, 로드 밸런싱, 서비스 검색과 같은 기능을 손쉽게 구현할 수 있습니다.

보안 및 네트워크 설정: Azure의 보안 그룹, 네트워크 설정을 통해 웹서버와 데이터베이스 간의 안전한 통신을 보장합니다. 또한 SSL/TLS를 통한 암호화된 데이터 전송을 설정합니다.

CI/CD 파이프라인 구축: Azure DevOps 또는 GitHub Actions와 같은 도구를 사용하여 지속적인 통합 및 배포(CI/CD) 파이프라인을 구성합니다. 이를 통해 코드 변경시 자동으로 테스트 및 배포가 이루어질 수 있도록 합니다.

