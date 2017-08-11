python -c "import sys; assert sys.version_info > (2, 6)"
if [ $? -eq 1 ]
then
    echo "Use python2.6+"
    exit 1
fi

python updateCapacity.py
python updatePledges.py
python updateDiskServersInIntervention.py
python updateDowntimes.py
python updateGgusTickets.py
python updateNotices.py
python updateStorageUsage_VO.py
python updateStorageUsage_MoreDetails.py
