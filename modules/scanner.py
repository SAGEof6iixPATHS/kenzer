#imports
import os
import time

#scanner
class Scanner:
    
    #initializations
    def __init__(self, domain, db, kenzer):
        self.domain = domain
        self.organization = domain
        self.path = db+self.organization
        self.resources = kenzer+"resources/"
        self.templates = self.resources+"kenzer-templates/"
        if(os.path.exists(self.path) == False):
            os.system("mkdir "+self.path)


    #helper modules

    #runs nuclei
    def nuclei(self, template, hosts, output):
        os.system("nuclei -stats -retries 2 -bulk-size 130 -rate-limit 80 -t {3}nuclei/{0} -timeout 8 -l {1} -o {2}".format(template, hosts, output, self.templates))
        return
    
    #runs jaeles
    def jaeles(self, template, hosts, output):
        os.system("jaeles scan --retry 2 --no-background -c 80 --rootDir {3}jaeles/ -s {3}jaeles/{0}/ --timeout 8 -U {1} -O {2} --no-db --chunk true ".format(template, hosts, output, self.templates))
        return

    #core modules

    #hunts for subdomain takeovers using nuclei
    def subscan(self):
        domain = self.domain
        path = self.path
        output = path+"/subscanWEB.log"
        subs = path+"/webenum.kenz"
        if(os.path.exists(subs) == False):
            return("!webenum")
        self.nuclei("subscan/web", subs, output)
        subs = path+"/subenum.kenz"
        if(os.path.exists(subs) == False):
            return("!subenum")
        output = path+"/subscanDNS.log"
        self.nuclei("subscan/dns/subdomain-takeover-dns.yaml", subs, output)
        output = path+"/subscanDNSWILD.log"
        self.nuclei("subscan/dns/subdomain-takeover-dns-wildcards.yaml", subs, output)
        out = path+"/subscan.kenz"
        if(os.path.exists(out)):
            os.system("mv {0} {0}.old".format(out))
        os.system("cat {0}/subscan* | sort -u > {1}".format(path, out))
        if(os.path.exists(out)):
            with open(out, encoding="ISO-8859-1") as f:
                line = len(f.readlines())
        else:
            line=0
        return line

    #hunts for CVEs using nuclei & jaeles
    def cvescan(self):
        domain = self.domain
        path = self.path
        subs = path+"/webenum.kenz"
        if(os.path.exists(subs) == False):
            return("!webenum")
        output = path+"/cvescanDOMN.log"
        self.nuclei("cvescan", subs, output)
        output = path+"/cvescanDOMJ.log"
        self.jaeles("cvescan", subs, output)
        out = path+"/cvescan.kenz"
        if(os.path.exists(out)):
            os.system("mv {0} {0}.old".format(out))
        os.system("cat {0}/cvescan* | sort -u > {1}".format(path, out))
        if(os.path.exists(out)):
            with open(out, encoding="ISO-8859-1") as f:
                line = len(f.readlines())
        else:
            line=0
        return line

    #hunts for vulnerabilities using nuclei & jaeles
    def vulnscan(self):
        domain = self.domain
        path = self.path
        subs = path+"/webenum.kenz"
        if(os.path.exists(subs) == False):
            return("!webenum")
        output = path+"/vulnscanDOMN.log"
        self.nuclei("vulnscan", subs, output)
        output = path+"/vulnscanDOMJ.log"
        self.jaeles("vulnscan", subs, output)
        out = path+"/vulnscan.kenz"
        if(os.path.exists(out)):
            os.system("mv {0} {0}.old".format(out))
        os.system("cat {0}/vulnscan* | sort -u > {1}".format(path, out))
        if(os.path.exists(out)):
            with open(out, encoding="ISO-8859-1") as f:
                line = len(f.readlines())
        else:
            line=0
        return line
    
    #scan with customized templates
    def cscan(self):
        domain = self.domain
        path = self.path
        subs = path+"/webenum.kenz"
        if(os.path.exists(subs) == False):
            return("!webenum")
        output = path+"/cscanDOMN.log"
        self.nuclei("cscan", subs, output)
        output = path+"/cscanDOMJ.log"
        self.jaeles("cscan", subs, output)
        out = path+"/cscan.kenz"
        if(os.path.exists(out)):
            os.system("mv {0} {0}.old".format(out))
        os.system("cat {0}/cscan* | sort -u > {1}".format(path, out))
        if(os.path.exists(out)):
            with open(out, encoding="ISO-8859-1") as f:
                line = len(f.readlines())
        else:
            line=0
        return line
    
    #hunts for vulnerabilities & CVEs in endpoints using nuclei & jaeles
    def endscan(self):
        domain = self.domain
        path = self.path
        subs = path+"/endpoints.kenz"
        if(os.path.exists(subs) == False):
            return("no endpoints found")        
        output = path+"/endscanVULN.log"
        self.nuclei("vulnscan", subs, output)
        output = path+"/endscanCVEN.log"
        self.nuclei("cvescan", subs, output)
        output = path+"/endscanVULJ.log"
        self.jaeles("vulnscan", subs, output)
        output = path+"/endscanCVEJ.log"
        self.jaeles("cvescan", subs, output)
        out = path+"/endscan.kenz"
        if(os.path.exists(out)):
            os.system("mv {0} {0}.old".format(out))
        os.system("cat {0}/endscan* | sort -u > {1}".format(path, out))
        if(os.path.exists(out)):
            with open(out, encoding="ISO-8859-1") as f:
                line = len(f.readlines())
        else:
            line=0
        return line
    

    #hunts for vulnerabilities in URLs with parameters using nuclei & jaeles
    def parascan(self):
        domain = self.domain
        path = self.path
        subs = path+"/urlenum.kenz"
        if(os.path.exists(subs) == False):
            return("!urlenum")
        params = path+"/params.log"
        os.system("cat {0} | gf params > {1}".format(subs, params))
        output = path+"/parascanN.log"
        self.nuclei("parascan", params, output)
        output = path+"/parascanJ.log"
        self.jaeles("parascan", params, output)
        out = path+"/parascan.kenz"
        if(os.path.exists(out)):
            os.system("mv {0} {0}.old".format(out))
        os.system("cat {0}/parascan* | sort -u > {1}".format(path, out))
        if(os.path.exists(out)):
            with open(out, encoding="ISO-8859-1") as f:
                line = len(f.readlines())
        else:
            line=0
        return line

    #hunts for unreferenced aws s3 buckets using S3Hunter
    def buckscan(self):
        domain = self.domain
        path = self.path
        subs = path+"/subenum.kenz"
        if(os.path.exists(subs) == False):
            return("!subenum")
        output = path+"/s3huntDirect.log"
        os.system("S3Hunter -l {0} -t 10  -T 60 -o {1} --only-direct".format(subs, output))
        output = path+"/iperms.log"
        os.system("S3Hunter --no-regions -l {0} -o {1} -P".format(subs, output))
        subs = output
        output = path+"/s3huntPerms.log"
        self.nuclei("subscan/web/S3Hunter.yaml", subs, output)
        out = path+"/buckscan.kenz"
        if(os.path.exists(out)):
            os.system("mv {0} {0}.old".format(out))
        os.system("cat {0}/s3hunt* | sort -u > {1}".format(path, out))
        if(os.path.exists(out)):
            with open(out, encoding="ISO-8859-1") as f:
                line = len(f.readlines())
        else:
            line=0
        return line
    
    #fingerprints probed servers using favinizer
    def favscan(self):
        domain = self.domain
        path = self.path
        out = path+"/favscan.kenz"
        subs = path+"/webenum.kenz"
        if(os.path.exists(subs) == False):
            return("!webenum")
        if(os.path.exists(out)):
            os.system("mv {0} {0}.old".format(out))
        os.system("favinizer -d {2}/favinizer.yaml -t 15 -T 60 -l {0} -o {1}".format(subs, out, self.templates))
        if(os.path.exists(out)):
            with open(out, encoding="ISO-8859-1") as f:
                line = len(f.readlines())
        else:
            line=0
        return line 
    
    #fingerprints probed servers using nuclei & jaeles
    def idscan(self):
        domain = self.domain
        path = self.path
        subs = path+"/webenum.kenz"
        if(os.path.exists(subs) == False):
            return("!webenum")
        output = path+"/idscanDOMN.log"
        self.nuclei("idscan", subs, output)
        output = path+"/idscanDOMJ.log"
        self.jaeles("idscan", subs, output)
        out = path+"/idscan.kenz"
        if(os.path.exists(out)):
            os.system("mv {0} {0}.old".format(out))
        os.system("cat {0}/idscan* | sort -u > {1}".format(path, out))
        if(os.path.exists(out)):
            with open(out, encoding="ISO-8859-1") as f:
                line = len(f.readlines())
        else:
            line=0
        return line
    
    #scans search engines & webpages for social media accounts
    def socscan(self):
        domain = self.domain
        path = self.path
        subs = path+"/webenum.kenz"
        if(os.path.exists(subs) == False):
            return("!webenum")
        output = path+"/EmailHarvester.log"
        os.system("EmailHarvester -d {0} -s {1}".format(domain, output))
        os.system("sed -i -e 's/^/[email] [{0}] /' {1}".format(domain, output))
        output = path+"/rescro.log"
        os.system("rescro -l {0} -s {1} -T 100 -o {2}".format(subs, self.templates+"rescro.yaml", output))
        out = path+"/socscan.kenz"
        if(os.path.exists(out)):
            os.system("mv {0} {0}.old".format(out))
        os.system("cat {0}/EmailHarvester.log {0}/rescro.log | sort -u  > {1}".format(path, out))
        if(os.path.exists(out)):
            with open(out, encoding="ISO-8859-1") as f:
                line = len(f.readlines())
        else:
            line=0
        return line
    
    #scans open ports using NXScan
    def portscan(self):
        domain = self.domain
        path = self.path
        out = path+"/portscan.kenz"
        subs = path+"/portenum.kenz"
        if(os.path.exists(subs) == False):
            return("!portenum")
        if(os.path.exists(out)):
            os.system("mv {0} {0}.old".format(out))
        os.system("sudo NXScan --only-scan -l {0} -o {1} -T {2}/nmap-bootstrap.xsl".format(subs,path+"/nxscan",self.templates))
        os.system("cp {0}/scan.html {1}".format(path+"/nxscan",out))
        if(os.path.exists(subs)):
            with open(subs, encoding="ISO-8859-1") as f:
                line = len(f.readlines())
        else:
            line=0
        return line
    
    #screenshots websites using aquatone
    def vizscan(self):
        domain = self.domain
        path = self.path
        out = path+"/vizscan.kenz"
        subs = path+"/webenum.kenz"
        if(os.path.exists(subs) == False):
            return("!webenum")
        if(os.path.exists(out)):
            os.system("mv {0} {0}.old".format(out))
        os.system("cat {0} | aquatone -threads=10 -http-timeout=15000 -resolution=\"720,480\" -save-body=false -out={1} -screenshot-timeout=200000".format(subs,path+"/aquatone"))
        os.system("cp {0}/aquatone_report.html {1}".format(path+"/aquatone",out))
        os.system("sed -i 's+screenshots/+aquatone/screenshots/+g' {0}".format(out))
        os.system("sed -i 's+headers/+aquatone/headers/+g' {0}".format(out))
        if(os.path.exists(subs)):
            with open(subs, encoding="ISO-8859-1") as f:
                line = len(f.readlines())
        else:
            line=0
        return line