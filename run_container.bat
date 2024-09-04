@echo off
:: Get the localhost IP address

for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /i "IPv4"') do set "LOCAL_IP=%%i"
set LOCAL_IP=%LOCAL_IP: =%

:: Pull the latest Docker image from the local registry
docker pull host.docker.internal:5001/python-etl-cv:latest

:: Run the Docker container with the specified environment variables
docker run -d --name python-etl-cv -p 80:80 ^
  -e MONGO_URI=mongodb://%LOCAL_IP%:27017 ^
  -e USERNAME_DB=mongodb ^
  -e PASSWORD_DB=mongodb123 ^
  -e DOMAIN_SELENIUM=http://%LOCAL_IP%:4444/wd/hub ^
  -e TESSERACT=/usr/bin/tesseract ^
  -e DATABASE_NM=database_info ^
  -e WEB_URL_TV365=https://timviec365.vn/nguoi-tim-viec.html ^
  -e COLLECTION_NM_TV365="info_detail" ^
  -e WEB_URL_ITVIEC=https://itviec.com/it-jobs ^
  -e COLLECTION_NM_ITVIEC="job_itviec" ^
  -e CONTENT_INFO_TV365="use_id,use_first_name,use_update_time,use_create_time,use_logo,use_gioi_tinh,use_birth_day,use_city,use_quanhuyen,use_address,use_hon_nhan,use_view,use_authentic,cv_title,cv_exp,cv_muctieu,cv_giai_thuong,cv_hoat_dong,cv_so_thich,cv_cate_id,cv_city_id,cv_district_id,cv_address,cv_capbac_id,cv_money_id,cv_loaihinh_id,cv_kynang,cv_tc_name,cv_tc_cv,cv_tc_phone,cv_tc_email,cv_tc_email,cv_video,cv_video_type,cv_hocvan,um_type,um_min_value,um_max_value,um_unit,profileDegree,profileNgoaiNgu,profileExperience" ^
  python-etl-cv:latest

echo "Container 'python-etl-cv' has been started."