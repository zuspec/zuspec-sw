#****************************************************************************
#* test_packed_structs.py
#*
#* Copyright 2023 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may 
#* not use this file except in compliance with the License.  
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software 
#* distributed under the License is distributed on an "AS IS" BASIS, 
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
#* See the License for the specific language governing permissions and 
#* limitations under the License.
#*
#* Created on:
#*     Author: 
#*
#****************************************************************************
import io
from zsp_arl_dm.core import Context
import zsp_be_sw.core as be_sw
from .test_base import TestBase

class TestPackedStructs(TestBase):

    def test_smoke(self):
        content = """
            import addr_reg_pkg::*;
            import std_pkg::*;

            struct my_s : packed_s<> {
                bit[4]      a;
                bit[12]     b;
            }

            pure component my_regs : reg_group_c {
                reg_c<my_s>       r1;
                reg_c<bit[32]>    r2;
                reg_c<my_s>       r3;
            }

            function void doit(my_regs s) {
                s.r1.write_val(0);
            }
        """

        self.enableDebug(True)
        ctxt : Context = self.loadContent(content)

        roots = []

        my_s = ctxt.findDataTypeStruct("my_s")
        self.assertIsNotNone(my_s)
        roots.append(my_s)

        my_regs = ctxt.findDataTypeComponent("my_regs")
        my_regs.getFields()[0].setAddrOffset(0)
        my_regs.getFields()[1].setAddrOffset(4)
        my_regs.getFields()[2].setAddrOffset(8)
        self.assertIsNotNone(my_regs)
        roots.append(my_regs)        

        doit_f = ctxt.findDataTypeFunction("doit")
        self.assertIsNotNone(doit_f)
        roots.append(doit_f)

        csrc = io.StringIO()
        pub_h = io.StringIO()
        prv_h = io.StringIO()

        # TODO: find 'my_s' 
        # TODO: pass to netlister

        be_sw_f = be_sw.Factory.inst()
        gen_ctxt = be_sw_f.mkContext(ctxt)
        be_sw_f.generateC(
            gen_ctxt,
            roots,
            csrc,
            pub_h,
            prv_h
        )

        print("csrc:\n%s" % csrc.getvalue())
        print("pub_h:\n%s" % pub_h.getvalue())
        print("prv_h:\n%s" % prv_h.getvalue())


        pass

