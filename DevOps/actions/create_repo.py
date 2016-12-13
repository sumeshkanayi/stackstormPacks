from st2actions.runners.pythonrunner import Action
import gitlab
import jenkins
import requests

class createPipeLine(Action):
      def run(self,repoName,Description):
	#Will create a Gitlab repository .Add a README.MD file with default contents and will create Master and Developmnt branches
        gitLabUrl=self.config["gitLabUrl"]
	gitLabUserName=self.config["gitLabUsername"]
        gitLabPassword=self.config["gitLabPassword"]
        jenkinsUrl=self.config["jenkinsUrl"]
        jenkinsUserName=self.config["jenkinsUserName"]
        jenkinsPassword=self.config["jenkinsPassword"]    
        connectGitLab = gitlab.Gitlab(gitLabUrl, email=gitLabUserName, password=gitLabPassword)	
        self.logger.info('Connecting to GitLab')
	connectGitLab.auth()
        self.logger.info(connectGitLab.auth())
        getAllGitLabProjects=connectGitLab.projects.list()
        print dir(getAllGitLabProjects[0]) 
        getAllGitLabProjectNames=[]
        for gitLabProject in getAllGitLabProjects:
		getAllGitLabProjectNames.append(gitLabProject.name) 
        if repoName in getAllGitLabProjectNames:
		 self.logger.error("Repo exists")
        else:    
		gitLabRepoCreationStatus=connectGitLab.projects.create({'name': repoName, 'default_branch': 'master', 'wiki_enabled': 1})
                self.logger.info('Created repo')
                self.logger.info(gitLabRepoCreationStatus)
		gitLabProjectId=gitLabRepoCreationStatus.id
		gitLabProjectSshUrl=gitLabRepoCreationStatus.ssh_url_to_repo
                self.logger.info('Creating gitFlow branches')                
		self.logger.info('Creating develop Branch')
                connectGitLab.project_files.create({'project_id' :gitLabProjectId,'file_path' :"README.md",'branch_name' :"master",'content':"This README file was Automatically generated .Please follow GitFlow branching model : https://yakiloo.com/getting-started-git-flow/",'commit_message':"Initial commit"})
                Jenkinsfilecontent=(open('/opt/stackstorm/packs/DevOps/actions/JenkinsFiles/SBT/Jenkinsfile').read())
                Jenkinsfile=connectGitLab.project_files.create({'project_id' :gitLabProjectId,'file_path' :"Jenkinsfile",'branch_name' :"master",'content': Jenkinsfilecontent,'commit_message':"Created a Jenkins File"})
		gitLabDevelopBranch=connectGitLab.project_branches.create({'branch_name': 'develop','ref': 'master', 'project_id' :gitLabProjectId})
                branches = connectGitLab.project_branches.list(project_id=gitLabProjectId)
		self.logger.info(branches)
		self.logger.info("GitLab repository creation completed")
	        self.logger.info("Starting Jenkins Job creation")
	
        def createJenkinsJob(jenkinsUrl,jenkinsUserName,jenkinsPassword):
            jenkinsConnection=jenkins.Jenkins(jenkinsUrl,jenkinsUserName,jenkinsPassword)
            jenkinsJobCreated=jenkinsConnection.build_job("dsl")
            self.logger.info('Jenkins job created')
            return jenkinsJobCreated	
	createJenkinsJob(jenkinsUrl,jenkinsUserName,jenkinsPassword)	



