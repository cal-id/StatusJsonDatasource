python -c "import sys; assert sys.version_info > (2,7)"
if [ $? -eq 1 ]
then
    echo "Use python2.7+"
    exit 1
fi

updateCapacity.py
updatePledges.py
python updateDiskServersInIntervention.py
python updateDowntimes.py
python updateGgusTickets.py
python updateNotices.py
python updateStorageUsageDataSource_VO.py
python updateStorageUsageDataSource_MoreDetails.py
python updateGanglia.py
