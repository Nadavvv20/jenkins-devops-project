pipeline {
    agent any 
    
    environment {
        // החלף את הערך למטה בשם המשתמש שלך ב-Docker Hub
        DOCKERHUB_USERNAME = 'nadavvv48'
        APP_NAME = 'jenkins-demo-app'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        registryCredential = 'docker-hub-credentials'
    }
    
    stages {
        stage('Checkout') {
            steps {
                // שלב זה קורה אוטומטית בפייפליין, אבל טוב לדעת שהוא קיים
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    // בניית האימג' ותיוג עם מספר הריצה הנוכחי
                    sh "docker build -t $DOCKERHUB_USERNAME/$APP_NAME:$IMAGE_TAG ."
                    // תיוג נוסף כ-latest
                    sh "docker tag $DOCKERHUB_USERNAME/$APP_NAME:$IMAGE_TAG $DOCKERHUB_USERNAME/$APP_NAME:latest"
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    echo 'Running Tests...'
                    // בדיקה פשוטה: האם הקונטיינר עולה ומדפיס את הגרסה של פייתון
                    // בתעשייה כאן נריץ Unit Tests אמיתיים
                    sh "docker run --rm $DOCKERHUB_USERNAME/$APP_NAME:$IMAGE_TAG python --version"
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    echo 'Pushing Docker Image...'
                    // שימוש בסיסמאות השמורות כדי להתחבר לדוקר
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh "echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin"
                        sh "docker push $DOCKERHUB_USERNAME/$APP_NAME:$IMAGE_TAG"
                        sh "docker push $DOCKERHUB_USERNAME/$APP_NAME:latest"
                    }
                }
            }
        }
	stage('Deploy to Production') {
            steps {
                script {
                    echo 'Deploying to Production Server...'
                    def prodIp = '172.31.6.189' // החלף ב-IP של שרת הפרודקשן
                    
                    // שימוש ב-SSH כדי להריץ פקודות מרחוק
                    // 1. עצירת הקונטיינר הישן (מתעלם משגיאה אם הוא לא קיים בזכות || true)
                    sh "ssh -o StrictHostKeyChecking=no ubuntu@${prodIp} 'docker stop $APP_NAME || true'"
                    sh "ssh -o StrictHostKeyChecking=no ubuntu@${prodIp} 'docker rm $APP_NAME || true'"
                    
                    // 2. משיכת הגרסה החדשה והרצה
                    // אנו מריצים בפורט 5000 וממפים אותו ל-5000
                    sh "ssh -o StrictHostKeyChecking=no ubuntu@${prodIp} 'docker run -d --name $APP_NAME -p 5000:5000 $DOCKERHUB_USERNAME/$APP_NAME:$IMAGE_TAG'"
                }
            }
        }
    }
    
    post {
        always {
            // ניקוי: מחיקת האימג'ים מהשרת של ג'נקינס כדי לא לסתום את הזיכרון
            // זה קריטי בשרתים קטנים כמו t2.micro
            sh "docker rmi $DOCKERHUB_USERNAME/$APP_NAME:$IMAGE_TAG || true"
            sh "docker rmi $DOCKERHUB_USERNAME/$APP_NAME:latest || true"
            echo 'Cleanup complete.'
        }
    }
}
