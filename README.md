## This repo is to update the repository variables set in bitbucket respoistories
basically this was setup to update the server ip variable so that when deploying it 
can help in direct and canary deployment to the server

```python
    1. create bitbucket application passowrd
    2. create .env file in the root directory
    3. create varibles to upage in .env file for eg:
        BITBUCKET_USERNAME=test
        BITBUCKET_APP_PASSWORD=test-keydfasdfasdfasdfafsdfasdf
        WORKSPACE_ID=test 
        REPO_SLUG=this-is-a-test-repo
        SERVER1=0.0.0.0
        SERVER2=0.0.0.1
        SERVER3=0.0.0.2
        SERVER4=0.0.0.3
        SERVER5=0.0.0.4
        SERVER6=0.0.0.5
        SERVER7=0.0.0.6
        SERVER8=0.0.0.7
        SERVER9=0.0.0.8
        SERVER10=0.0.0.9
    4. pip install -r requirements.txt
    5. python update.py

```

## versions
```
python version >= 3.6.5
```
