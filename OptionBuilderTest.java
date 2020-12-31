/**
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.commons.cli;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import org.junit.Test;

@SuppressWarnings("deprecation") // OptionBuilder is marked deprecated
public class OptionBuilderTest
{   
    /**
     *  1. Creates a new Option using OptionBuilder and checks its opt, long opt,
     *     description, type, arg, if its required and its args.
     */
    @Test
    public void testCompleteOption( ) {
        Option simple = OptionBuilder.withLongOpt( "simple option")
                                     .hasArg( )
                                     .isRequired( )
                                     .hasArgs( )
                                     .withType( Float.class )
                                     .withDescription( "this is a simple option" )
                                     .create( 's' );

        assertEquals( "s", simple.getOpt() );
        assertEquals( "simple option", simple.getLongOpt() );
        assertEquals( "this is a simple option", simple.getDescription() );
        assertEquals( simple.getType(), Float.class );
        assertTrue( simple.hasArg() );
        assertTrue( simple.isRequired() );
        assertTrue( simple.hasArgs() );
    }

    /**
     * 1. Creates a new Option "simple" using OptionBuilder and checks its
     *    opt, long opt, description, type, arg, if it is required and its args.
     * 2. Creates a new Option using OptionBuilder and assigns it to "simple", and
     *    checks its opt, long opt, description, type, arg, if it is required and
     *     its args.
     */
    @Test
    public void testTwoCompleteOptions( ) {
        Option simple = OptionBuilder.withLongOpt( "simple option")
                                     .hasArg( )
                                     .isRequired( )
                                     .hasArgs( )
                                     .withType( Float.class )
                                     .withDescription( "this is a simple option" )
                                     .create( 's' );

        assertEquals( "s", simple.getOpt() );
        assertEquals( "simple option", simple.getLongOpt() );
        assertEquals( "this is a simple option", simple.getDescription() );
        assertEquals( simple.getType(), Float.class );
        assertTrue( simple.hasArg() );
        assertTrue( simple.isRequired() );
        assertTrue( simple.hasArgs() );

        simple = OptionBuilder.withLongOpt( "dimple option")
                              .hasArg( )
                              .withDescription( "this is a dimple option" )
                              .create( 'd' );

        assertEquals( "d", simple.getOpt() );
        assertEquals( "dimple option", simple.getLongOpt() );
        assertEquals( "this is a dimple option", simple.getDescription() );
        assertEquals( String.class, simple.getType() );
        assertTrue( simple.hasArg() );
        assertTrue( !simple.isRequired() );
        assertTrue( !simple.hasArgs() );
    }

    /**
     * 1. Creates a new Option using OptionBuiilder and checks its opt, description and if it
     *    has arg.
     */
    @Test
    public void testBaseOptionCharOpt() {
        Option base = OptionBuilder.withDescription( "option description")
                                   .create( 'o' );

        assertEquals( "o", base.getOpt() );
        assertEquals( "option description", base.getDescription() );
        assertTrue( !base.hasArg() );
    }

    /**
     * 1. Creates a new Option using OptionBuiilder and checks its opt, description and if it
     *    has arg.
     */
    @Test
    public void testBaseOptionStringOpt() {
        Option base = OptionBuilder.withDescription( "option description")
                                   .create( "o" );

        assertEquals( "o", base.getOpt() );
        assertEquals( "option description", base.getDescription() );
        assertTrue( !base.hasArg() );
    }

    /**
     * 1. Creates two Options using OptionBuilder and checks their opt.
     * 2. Expects an IllegalArgumentException when calling method create of OptionBuilder
     *    with argument " ".
     */
    @Test
    public void testSpecialOptChars() throws Exception
    {
        // '?'
        Option opt1 = OptionBuilder.withDescription("help options").create('?');
        assertEquals("?", opt1.getOpt());

        // '@'
        Option opt2 = OptionBuilder.withDescription("read from stdin").create('@');
        assertEquals("@", opt2.getOpt());
        
        // ' '
        try {
            OptionBuilder.create(' ');
            fail( "IllegalArgumentException not caught" );
        } catch (IllegalArgumentException e) {
            // success
        }
    }

    /**
     * 1. Creates a new Option using OptionBuilder and checks if its args equals 2.
     */
    @Test
    public void testOptionArgNumbers()
    {
        Option opt = OptionBuilder.withDescription( "option description" )
                                  .hasArgs( 2 )
                                  .create( 'o' );
        assertEquals( 2, opt.getArgs() );
    }

    /**
     * 1. Expects an IllegalArgumentException when calling chained methods of OptionBuilder.
     * 2. Expects an IllegalArgumentException when calling method create of OptionBuilder with
     *    argument "opt`".
     * 3. Expects an IllegalArgumentException when calling method create of OptionBuilder with
     *    argument "opt". 
     * Note: We need to fix this description it is wrong currently.
     */
    @Test
    public void testIllegalOptions() {
        // bad single character option
        try {
            OptionBuilder.withDescription( "option description" ).create( '"' );
            fail( "IllegalArgumentException not caught" );
        }
        catch( IllegalArgumentException exp ) {
            // success
        }

        // bad character in option string
        try {
            OptionBuilder.create( "opt`" );
            fail( "IllegalArgumentException not caught" );
        }
        catch( IllegalArgumentException exp ) {
            // success
        }

        // valid option 
        try {
            OptionBuilder.create( "opt" );
            // success
        }
        catch( IllegalArgumentException exp ) {
            fail( "IllegalArgumentException caught" );
        }
    }

    /**
     * 1. Expects an IllegalArgumentException when calling chained methods of OptionBuilder.
     * Note: This is wrong as well.
     */
    @Test
    public void testCreateIncompleteOption() {
        try
        {
            OptionBuilder.hasArg().create();
            fail("Incomplete option should be rejected");
        }
        catch (IllegalArgumentException e)
        {
            // expected
            
            // implicitly reset the builder
            OptionBuilder.create( "opt" );
        }
    }

    /**
     * 1. Expects an IllegalArgumentException when calling chained methods of OptionBuilder.
     * 2. Checks if the result of chained methods of OptionBuilder is not null.
     * 3. Expects IllegalArgumentException when calling chained methods of OptionBuilder.
     * 4. Checks if the result of calling chained methds of OptionBuilder is not null.
     */
    @Test
    public void testBuilderIsResettedAlways() {
        try
        {
            OptionBuilder.withDescription("JUnit").create('"');
            fail("IllegalArgumentException expected");
        }
        catch (IllegalArgumentException e)
        {
            // expected
        }
        assertNull("we inherited a description", OptionBuilder.create('x').getDescription());

        try
        {
            OptionBuilder.withDescription("JUnit").create();
            fail("IllegalArgumentException expected");
        }
        catch (IllegalArgumentException e)
        {
            // expected
        }
        assertNull("we inherited a description", OptionBuilder.create('x').getDescription());
    }
}
