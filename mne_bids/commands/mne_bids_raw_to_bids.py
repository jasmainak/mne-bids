#!/usr/bin/env python
# Authors: Teon Brooks  <teon.brooks@gmail.com>

"""Command line interface for mne_bids.

example usage:  $ mne_bids raw_to_bids --subject_id sub01 --task rest
--raw_fname data.edf --output_path new_path

"""
import os
from mne_bids import write_raw_bids, make_bids_filename
from mne_bids.io import read_raw


def run():
    """Run command."""
    from mne.commands.utils import get_optparser

    parser = get_optparser(__file__)

    parser.set_defaults(kind='meg')
    parser.add_option('--subject_id', dest='subject_id',
                      help=('The subject name in BIDS compatible format',
                            '(01,02, etc.)'), metavar='s')
    parser.add_option('--task', dest='task',
                      help='Name of the task the data is based on.',
                      metavar='t')
    parser.add_option('--raw_fname', dest='raw_fname',
                      help='The path to the raw MEG file.', metavar='r')
    parser.add_option('--output_path', dest='output_path',
                      help='The path of the BIDS compatible folder.',
                      metavar='o')
    parser.add_option('--session_id', dest='session_id',
                      help='The session name in BIDS compatible format.',
                      metavar='ses')
    parser.add_option('--run', dest='run',
                      help='The run number for this dataset.',
                      metavar='run')
    parser.add_option('--acq', dest='acq',
                      help='The acquisition parameter.',
                      metavar='acq')
    parser.add_option('--kind', dest='kind',
                      help='The kind of data being converted.',
                      metavar='k')
    parser.add_option('--events_data', dest='events_data',
                      help='The events file.', metavar='evt')
    parser.add_option('--event_id', dest='event_id',
                      help='The event id dict.', metavar='eid')
    parser.add_option('--hpi', dest='hpi',
                      help='The path to the MEG Marker points',
                      metavar='filename')
    parser.add_option('--electrode', dest='electrode',
                      help='The path to head-native Digitizer points',
                      metavar='elec')
    parser.add_option('--hsp', dest='hsp',
                      help='The path to headshape points.', metavar='hsp')
    parser.add_option('--config', dest='config',
                      help='The path to the configuration file', metavar='cfg')
    parser.add_option('--overwrite', dest='overwrite',
                      help=("Boolean. Whether to overwrite existing data"),
                      metavar='ow')

    opt, args = parser.parse_args()

    suffix = '%s%s' % (opt.kind, os.path.splitext(opt.raw_fname)[1])
    bids_fname = make_bids_filename(
        subject=opt.subject_id, session=opt.session_id, run=opt.run,
        acquisition=opt.acq, task=opt.task, suffix=suffix)
    raw = read_raw(opt.raw_fname, hpi=opt.hpi, electrode=opt.electrode,
                   hsp=opt.hsp, config=opt.config)
    write_raw_bids(raw, bids_fname, opt.output_path, event_id=opt.event_id,
                   kind=opt.kind, events_data=opt.events_data,
                   overwrite=opt.overwrite, verbose=True)


is_main = (__name__ == '__main__')
if is_main:
    run()
