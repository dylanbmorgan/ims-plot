class file_parser_qctddft(file_parser_libwfa):
    def read(self, mos):
        """
        Read the X vector from standard output. Y is discarded.
        """
        state_list = []
        exc_diff = exc_1TDM = tdread = libwfa = False
        istate = 0

        self.state_list_om = self.rmatfile_one()

        if self.ioptions.get('TDA'):
            ststr  = 'TDDFT/TDA Excitation Energies'
            ststr2 = 'CIS Excitation Energies'
        else:
            ststr  = 'TDDFT Excitation Energies'
            ststr2 = 'xyzabc' # dummy string

        print("Parsing %s for %s ..."%(self.ioptions.get('rfile'), ststr))

        nsing = 0
        ntrip = 0
        rfileh = open(self.ioptions.get('rfile'),'r') 
        while True: # loop over all lines
            try:
                line = next(rfileh)
            except StopIteration:
              print("Finished parsing file %s"%self.ioptions.get('rfile'))
              break

            if ststr in line or ststr2 in line:
                tdread = True
                line = next(rfileh)
            elif 'TDDFT calculation will be performed' in line:
                tdread = False
            elif '-----' in line:
                tdread = False
            elif 'Excited State Analysis' in line:
                tdread = False
                libwfa = True
                if len(state_list) == 0:
                    errstr = "No excitation energy parsed!"
                    errstr+= "\n   Please, set 'TDA=True' if this was a TDA calculation."
                    raise error_handler.MsgError(errstr)
            elif 'SA-NTO Decomposition' in line:
                libwfa = False
            elif 'Welcome to Q-Chem' in line:
                if len(state_list) > 0:
                    print("\n WARNING: found second Q-Chem job!\n   Deleting everything parsed so far.\n")

                state_list = []
                exc_diff = exc_1TDM = tdread = libwfa = False
                istate = 0

            if tdread:
                words = line.replace(':','').split()
                if 'Excited state' in line:
                    state_list.append({})
                    state = state_list[-1]

                    state['state_num'] = int(words[2])
                    state['exc_en'] = float(words[-1])

                    line = next(rfileh)
                    line = next(rfileh)
                    words = line.split()

                    if words[0] == 'Multiplicity:':
                        state['mult'] = words[1]
                    else:
                        state['mult'] = 'X'

                    if state['mult'] == 'Singlet':
                        nsing += 1
                        state['name'] = "S_%i"%nsing
                        state['lname'] = "Singlet %i"%nsing
                    elif state['mult'] == 'Triplet':
                        ntrip += 1
                        state['name'] = "T_%i"%ntrip
                        state['lname'] = "Triplet %i"%ntrip
                    else:
                        state['name'] = 'es_%i'%(state['state_num'])
                        state['lname'] = 'Excited State %i'%(state['state_num'])

                    if self.ioptions['read_libwfa']:
                        om_at = None
                        for ostate in self.state_list_om:
                            if ostate['lname'] == state['lname']:
                                om_at = ostate['OmAt']

                        if om_at is None:
                            if os.path.exists('%s_ctnum_atomic.om'%state['name']):
                                (typ, exctmp, osc, num_at, num_at1, om_at) = self.rmatfile('%s_ctnum_atomic.om'%state['name'])
                            elif os.path.exists('%s_ctnum_mulliken.om'%state['name']):
                                (typ, exctmp, osc, num_at, num_at1, om_at) = self.rmatfile('%s_ctnum_mulliken.om'%state['name'])
                            elif os.path.exists('%s_ctnum_lowdin.om'%state['name']):
                                (typ, exctmp, osc, num_at, num_at1, om_at) = self.rmatfile('%s_ctnum_lowdin.om'%state['name'])

                        if not om_at is None:
                            state_list[-1]['Om']   = om_at.sum()
                            state_list[-1]['OmAt'] = om_at
                    else:
                        state_list[-1]['tden'] = self.init_den(mos, rect=True)

                elif 'Strength' in line:
                    state_list[-1]['osc_str'] = float(words[-1])

                elif 'amplitude' in line and not self.ioptions['read_libwfa']:
                    # ignore the Y vector.
                    #    Otherwise the Y would go into the virt-occ block!
                    if 'Y:' in line: continue

                    awords = self.delete_chars(line, ['X:', 'Y:', 'D', 'V', '(', ')', '-->'])

                    iocc = int(awords[0]) - 1
                    ivirt = int(awords[1]) + mos.ret_ihomo()

                    coeff =  float(awords[4])

                    state_list[-1]['tden'][iocc, ivirt] += coeff

            if libwfa:
                if 'Excited state' in line:
                    words = line.replace(':', '').split()
                    istate = int(words[2]) - 1

                # Disentangle the order of singlets and triplets
                elif '  Singlet' in line or '  Triplet' in line:
                    words = line.split()
                    currname = words[0][0] + "_" + words[1]
                    for istate, state in enumerate(state_list):
                        if state['name'] == currname:
                            break
                    else:
                        raise error_handler.MsgError("Did not find state %s"%currname)

                elif 'Exciton analysis of the difference density matrix' in line:
                    exc_1TDM = False
                    exc_diff = True

                elif 'Exciton analysis of the transition density matrix' in line:
                    exc_diff = False
                    exc_1TDM = True

                self.parse_keys(state_list[istate], exc_diff, exc_1TDM, line)

        rfileh.close()
        return state_list