from minyaneto.config.release import Config
from minyaneto.service.dal.search_svc import Dao

if __name__ == '__main__':
    dao = Dao(Config.ES_HOSTS, is_test=False)
    ids = ['AWHwwinfXhnPh-4nqCEB','AWHxmFfAXhnPh-4nqCEQ','AWHxk9rdXhnPh-4nqCEP','AWGET0YlG6LZz5SyOc-8','AWGD2GYZG6LZz5SyOc-0','AWHwy_PAXhnPh-4nqCEG','AWD6_pxCG6LZz5SyOc9l','AWG1HLy1XhnPh-4nqCDK','AWG4fKGoXhnPh-4nqCDR','AWHwx3L-XhnPh-4nqCED','AWHw1b3aXhnPh-4nqCEK','AWDSt_nSG6LZz5SyOc9i','AWDStpesG6LZz5SyOc9h','AWEIQfQeG6LZz5SyOc9r','AWEIPMLJG6LZz5SyOc9p','AWD6_qmPG6LZz5SyOc9m','AWHwxiJ2XhnPh-4nqCEC','AWHwyzZyXhnPh-4nqCEF','AWDSs_OOG6LZz5SyOc9g','AWDSp-fTG6LZz5SyOc9c','AWHw3zz6XhnPh-4nqCEM','AWFRirnUG6LZz5SyOc95','AWFRirrDG6LZz5SyOc96','AWFRiqY9G6LZz5SyOc91','AWFRi5UMG6LZz5SyOc-J','AWFRi5VaG6LZz5SyOc-K','AWFRin0nG6LZz5SyOc9v','AWFRtqlBG6LZz5SyOc-V','AWFRtqxnG6LZz5SyOc-a','AWFRi3FdG6LZz5SyOc-A','AWFRi3EKG6LZz5SyOc9_','AWFRijhFG6LZz5SyOc9u','AWFRiqSGG6LZz5SyOc9y','AWFRiqWsG6LZz5SyOc90','AWFRiramG6LZz5SyOc94','AWFRiruZG6LZz5SyOc97','AWFRi2_iG6LZz5SyOc9-','AWFRi3KuG6LZz5SyOc-C','AWFRi5SwG6LZz5SyOc-I','AWFRtqumG6LZz5SyOc-Z']
    for id in ids:
        print 'deleting: ' + str(id)
        dao.delete_synagogue(id)

    print 'done'



