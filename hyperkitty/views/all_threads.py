#-*- coding: utf-8 -*-
# Copyright (C) 2014-2015 by the Free Software Foundation, Inc.
#
# This file is part of HyperKitty.
#
# HyperKitty is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# HyperKitty is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# HyperKitty.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Aurelien Bompard <abompard@fedoraproject.org>
#

import datetime
import json
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from hyperkitty.models import Favorite, MailingList

def subject_lines(request, mlist):
    """ Gets the number of unique subject lines for mlist"""

    d = (datetime.date.today()).replace(day=1)
    stop_date = d - datetime.timedelta(days=1)  
    start_date = stop_date.replace(day=1)
    mlist = get_object_or_404(MailingList, name=mlist)
    threads = mlist.get_threads_between(start_date, stop_date)
   
    result = {"The count of unique subject lines are ":threads.count()}
   
    return HttpResponse(json.dumps(result),
                        content_type="application/json")


def members_who_posted(request, mlist):
    """Gets the sunscribers who posted on mlist"""

    d = (datetime.date.today()).replace(day=1)
    stop_date = d - datetime.timedelta(days=1)
    start_date = stop_date.replace(day=1)
    mlist = get_object_or_404(MailingList, name=mlist)
    members = mlist.get_participants(start_date, stop_date)
    member_count = mlist.get_participants_count_between(start_date, stop_date)
    
    result = {"The members who posted are ": [str(obj['sender_id']) for obj in members.values()]}
    result_count = {"The number of members who posted are ": member_count}
   
    return HttpResponse(json.dumps([result,result_count]),
                        content_type="application/json")




