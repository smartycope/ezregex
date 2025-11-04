#!/usr/bin/env perl
# use strict;
use warnings;
use JSON::PP;  # core module since Perl 5.14

# Read JSON file
my $filename = 'data/compiled_regexs.json';
open my $fh, '<', $filename or die "Cannot open $filename: $!";
my $json_text = do { local $/; <$fh> };
close $fh;

my $data = decode_json($json_text);
my $regexs = $data->{perl};

sub myassert {
    my ($b, $should_be, $i, $failing) = @_;
    if ($b != $should_be) {
        print "\n----------------------- TEST FAILED -----------------------\n";
        print "language       = `perl`\n";
        print "pattern        = `$i->{ezregex}`\n";
        print "compiled regex = `$i->{regex}`\n";
        $failing =~ s/\n/\\n/g;
        print "pattern should " . ($should_be ? "" : "NOT ") . "match `$failing`\n";
        exit 1;
    }
}

for my $i (@$regexs) {
    for my $m (@{$i->{should}}) {
        myassert($m =~ /$i->{regex}/, 1, $i, $m);
    }
    for my $m (@{$i->{shouldnt}}) {
        myassert($m =~ /$i->{regex}/, 0, $i, $m);
    }
}

print "pass\n";
