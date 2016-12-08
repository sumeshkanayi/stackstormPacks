from st2actions.runners.pythonrunner import Action
import gitlab
import jenkins
import requests

class createPipeLine(Action):
      def run(self,repoName):
	#Will create a Gitlab repository .Add a README.MD file with default contents and will create Master and Developmnt branches
        gitLabUrl=self.config["gitLabUrl"]
	gitLabUserName=self.config["gitLabUsername"]
        gitLabPassword=self.config["gitLabPassword"]
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
		gitLabDevelopBranch=connectGitLab.project_branches.create({'branch_name': 'develop','ref': 'master', 'project_id' :gitLabProjectId})
                branches = connectGitLab.project_branches.list(project_id=gitLabProjectId)
		self.logger.info(branches)
		self.logger.info("GitLab repository creation completed")
	        self.logger.info("Starting Jenkins Job creation")
	
	 def createJenkinsJob(jenkinsUrl,jenkinsUserName,jenkinsPassword,jenkinsTemplate,repositoryUrl):
            jenkinsConnection=jenkins.Jenkins(jenkinsUrl,jenkinsUserName,jenkinsPassword)
            jenkinsJobGitRepo='<url>'+repositoryUrl+'</url>'
            jenkinsJobDescription='<description>'+description+'</description>'
            jenkinsTemplateConfig=jenkinsConnection.get_job_config(jenkinsTemplate)
            jenkinsTemplateUpdatedDescription=jenkinsTemplateConfig.replace('<description>This is a template maven project</description>',jenkinsJobDescription)
            jenkinsTemplateUpdateWithGit=jenkinsTemplateUpdatedDescription.replace('<url>http://10.205.36.84:8443/r/om.rxcorp.maven.template.git</url>',jenkinsJobGitRepo)
            self.logger.info("Update Jenkins XML: %s", jenkinsTemplateUpdateWithGit)
            jenkinsJobCreated=jenkinsConnection.create_job(semanticName,jenkinsTemplateUpdateWithGit)
            self.logger.info('Jenkins Template Job : %s', jenkinsTemplateConfig)
            return jenkinsJobCreated	
		



