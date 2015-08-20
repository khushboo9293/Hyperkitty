# -*- coding: utf-8 -*-
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

from __future__ import absolute_import, print_function, unicode_literals

import uuid
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from mock import Mock

from hyperkitty.lib import posting
from hyperkitty.lib.mailman import FakeMMList, FakeMMMember
from hyperkitty.models import MailingList
from hyperkitty.tests.utils import TestCase


class PostingTestCase(TestCase):

    def setUp(self):
        self.mlist = MailingList.objects.create(name="list@example.com")
        self.ml = FakeMMList("list@example.com")
        self.mailman_client.get_list.side_effect = lambda n: self.ml
        #self.ml.get_member = Mock()
        #self.ml.subscribe = Mock()
        self.user = User.objects.create_user(
            'testuser', 'testuser@example.com', 'testPass')
        self.mm_user = Mock()
        self.mailman_client.get_user.side_effect = lambda name: self.mm_user
        self.mm_user.user_id = uuid.uuid1().int
        self.mm_user.addresses = ["testuser@example.com"]
        self.mm_user.subscriptions = []
        self.request = RequestFactory().get("/")
        self.request.user = self.user

    def test_sender_not_subscribed(self):
        self.assertEqual(posting.get_sender(self.request, self.mlist),
                         "testuser@example.com")

    def test_sender_with_display_name(self):
        self.user.first_name = "Test"
        self.user.last_name = "User"
        self.assertEqual(posting.get_sender(self.request, self.mlist),
                         '"Test User" <testuser@example.com>')

    def test_sender_subscribed(self):
        self.mm_user.subscriptions = [
            FakeMMMember(self.mlist.name, "secondemail@example.com"),
        ]
        self.assertEqual(posting.get_sender(self.request, self.mlist),
                         "secondemail@example.com")

