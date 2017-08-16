import ldap
import ldap.modlist as modlist
import uuid
import sys

user = sys.argv[1]
passw = sys.argv[2]
gid = sys.argv[3]


try:
        l = ldap.initialize("ldap://127.0.0.1:389")
        l.protocol_version = ldap.VERSION3
        l.simple_bind_s(user,passw);
        result = l.search_s("dc=econo",ldap.SCOPE_SUBTREE,"(gidNumber=" + gid + ")",["gidNumber",'uidNumber'])
        lastNumber = 0

        if result != None:
            for dn,n in result:
                print dn
                print n

            	sambaSID = 'S-1-5-21-69815507-558479685-3467165442-' + gid

                cn = gid
            	mod_attrs = [('cn', cn),
            		     ('gidNumber', gid),
            		     ('sambaSID',sambaSID),
            		     ('sambaGroupType','2'),
            		     ('objectClass', ['top','posixGroup','sambaGroupMapping'])
            	]


            	dn = "cn=" + cn + ",ou=groups,dc=econo"
                l.add_s(dn,mod_attrs)

        l.unbind_s()

        sys.exit(1)

        """
    	gid = str(lastNumber + 1)
    	sambaSID = 'S-1-5-21-69815507-558479685-3467165442-' + gid


    	mod_attrs = [('cn', cn),
    		     ('gidNumber', gid),
    		     ('mail', mail),
    		     ('sambaSID',sambaSID),
    		     ('sambaGroupType','2'),
    		     ('acl', 'anyone p'),
    		     ('gosaMailServer','smtp'),
    		     ('gosaMailDeliveryMode','[L]'),
    		     ('gosaSharedFolderTarget','share.' + mail),
    		     ('objectClass', ['top','posixGroup','gosaMailAccount','sambaGroupMapping'])
    	]


    	dn = "cn=" + cn + ",ou=groups,dc=econo"
            l.add_s(dn,mod_attrs)

            l.unbind_s()
        """
except ldap.LDAPError, e:
        print e
